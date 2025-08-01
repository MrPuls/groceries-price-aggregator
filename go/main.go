package main

import (
	"encoding/csv"
	"encoding/json"
	"fmt"
	"io"
	"log"
	"net/http"
	"net/url"
	"os"
)

type CategoryItem struct {
	Slug string `json:"slug"`
}

type Categories struct {
	Total int64          `json:"total"`
	Items []CategoryItem `json:"items"`
}

type CategoryDetails struct {
	Title string `json:"title"`
}

type ProductDetails struct {
	Title        string  `json:"title"`
	SectionSlug  string  `json:"sectionSlug"`
	DisplayPrice float64 `json:"displayPrice"`
	DisplayRatio string  `json:"displayRatio"`
}

type Product struct {
	Total int64            `json:"total"`
	Items []ProductDetails `json:"items"`
}

type ProductDescription struct {
	Name     string
	Ref      string
	Price    string
	Category string
	Shop     string
}

func makeRequest(reqUrl string, params map[string]string) (resp *http.Response, err error) {
	// TODO: create client as a type method
	client := &http.Client{}
	if params != nil {
		p := url.Values{}
		for k, v := range params {
			p.Add(k, v)
		}
		queryString := p.Encode()

		reqUrl = fmt.Sprintf("%s?%s", reqUrl, queryString)
	}

	req, err := http.NewRequest("GET", reqUrl, nil)
	if err != nil {
		panic(err)
	}

	req.Header.Add("Accept", "application/json")
	req.Header.Add("Accept-Encoding", "utf-8")
	req.Host = "sf-ecom-api.silpo.ua"
	req.Header.Add("Origin", "https://silpo.ua")
	req.Header.Add("Referer", "https://silpo.ua/")
	req.Header.Add("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:140.0) Gecko/20100101 Firefox/140.0")
	req.Header.Add("Sec-Fetch-Mode", "cors")
	req.Header.Add("Sec-Fetch-Site", "same-site")
	req.Header.Add("Sec-Fetch-Dest", "empty")
	req.Header.Add("Sec-GPC", "1")
	req.Header.Add("TE", "trailers")
	req.Header.Add("Accept-Language", "en-GB,en;q=0.5")
	resp, respErr := client.Do(req)
	if respErr != nil {
		return nil, respErr
	}

	return resp, nil
}

func getCategories() ([]string, error) {
	categoriesUrl := "https://sf-ecom-api.silpo.ua/v1/branches/00000000-0000-0000-0000-000000000000/categories/tree"
	params := map[string]string{
		"deliveryType": "DeliveryHome",
		"depth":        "1",
	}
	resp, respErr := makeRequest(categoriesUrl, params)
	if respErr != nil {
		return nil, respErr
	}
	defer resp.Body.Close()
	bb, _ := io.ReadAll(resp.Body)

	var c Categories
	rb := json.Unmarshal(bb, &c)
	if rb != nil {
		panic(rb)
	}
	var ra []string
	for _, v := range c.Items {
		ra = append(ra, v.Slug)
	}
	return ra, nil
}

func getCategoriesTitles(cts []string) (map[string]string, error) {
	categoryDetailsUrl := "https://sf-ecom-api.silpo.ua/v1/uk/branches/00000000-0000-0000-0000-000000000000/categories/"
	result := map[string]string{}
	for _, ct := range cts {
		ctUrl := fmt.Sprintf("%s%s", categoryDetailsUrl, ct)
		resp, err := makeRequest(ctUrl, nil)
		if err != nil {
			return nil, err
		}
		defer resp.Body.Close()
		bb, _ := io.ReadAll(resp.Body)
		var cd CategoryDetails
		rb := json.Unmarshal(bb, &cd)
		if rb != nil {
			return nil, rb
		}

		result[ct] = cd.Title
	}
	return result, nil
}
func getProducts(ctg map[string]string) ([][]string, error) {
	productsUrl := "https://sf-ecom-api.silpo.ua/v1/uk/branches/00000000-0000-0000-0000-000000000000/products"
	var result [][]string
	// TODO: Works, but need to parallelize to goroutines, increase offset.
	// 	Also should fix the defer in loop leaks due to each request will be in separate goroutine
	for slug, title := range ctg {
		params := map[string]string{
			"deliveryType":           "DeliveryHome",
			"category":               slug,
			"includeChildCategories": "true",
			"sortBy":                 "popularity",
			"sortDirection":          "desc",
			"inStock":                "false",
			"limit":                  "100",
			"offset":                 "0",
		}
		resp, respErr := makeRequest(productsUrl, params)
		if respErr != nil {
			return nil, respErr
		}
		defer resp.Body.Close()
		bb, _ := io.ReadAll(resp.Body)
		var pr Product
		rb := json.Unmarshal(bb, &pr)
		if rb != nil {
			return nil, rb
		}
		fmt.Println(pr.Total)
		for _, v := range pr.Items {
			result = append(result, []string{
				v.Title,
				fmt.Sprintf("https://silpo.ua/product/%s", v.SectionSlug),
				fmt.Sprintf("%.2f грн/%s", v.DisplayPrice, v.DisplayRatio),
				title,
				"silpo",
			})
		}
	}
	return result, nil
}

func main() {
	log.Println("Starting main program")
	cts, err := getCategories()
	if err != nil {
		panic(err)
	}

	ctts, tErr := getCategoriesTitles(cts)
	if tErr != nil {
		panic(tErr)
	}

	fmt.Println(cts)
	fmt.Println(ctts)
	products, pErr := getProducts(ctts)
	if pErr != nil {
		panic(err)
	}

	records := [][]string{
		{"Name", "Ref", "Price", "Category", "Shop"},
	}

	// Create the CSV file
	file, err := os.Create("output.csv")
	if err != nil {
		log.Fatal("Error creating file:", err)
	}
	defer file.Close() // Ensure the file is closed when the function exits

	// Create a new CSV writer
	writer := csv.NewWriter(file)
	defer writer.Flush() // Ensure any buffered data is written to the file

	// Write all records to the CSV file
	for _, record := range records {
		if err := writer.Write(record); err != nil {
			log.Fatal("Error writing record to CSV:", err)
		}
		if err := writer.WriteAll(products); err != nil {
			log.Fatal("Error writing record to CSV:", err)
		}
	}

	log.Println("Data successfully written to output.csv")
}
