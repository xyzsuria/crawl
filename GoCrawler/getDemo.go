package main

import (
	"bufio"
	"bytes"
	"fmt"
	"github.com/antchfx/htmlquery"
	"golang.org/x/net/html/charset"
	"golang.org/x/text/encoding"
	"golang.org/x/text/encoding/unicode"
	"golang.org/x/text/transform"
	"io/ioutil"
	"net/http"
)

func FetchV(url string) ([]byte, error) {
	resp, err := http.Get(url)
	if err != nil {
		panic(err)
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		fmt.Printf("Error status code: %v", resp.StatusCode)
	}
	bodyReader := bufio.NewReader(resp.Body)
	e := DerterminEncodingV(bodyReader) //utf-8
	utf8Reader := transform.NewReader(bodyReader, e.NewDecoder())
	return ioutil.ReadAll(utf8Reader)
}

func DerterminEncodingV(r *bufio.Reader) encoding.Encoding {
	bytes, err := r.Peek(1024)

	if err != nil {
		fmt.Printf("fetch error: %v", err)
		return unicode.UTF8
	}

	e, _, _ := charset.DetermineEncoding(bytes, "")
	return e
}

func main() {
	url := "https://www.thepaper.cn/"
	body, err := FetchV(url)

	if err != nil {
		fmt.Println("read content failed:%v", err)
		return
	}
	doc, err := htmlquery.Parse(bytes.NewReader(body))
	if err != nil {
		fmt.Println("htmlquery.Parse failed:%v", err)
	}
	nodes := htmlquery.Find(doc, `//div[@class="small_cardcontent__BTALp"]/h2`)

	for _, node := range nodes {
		fmt.Println("fetch card ", node.FirstChild.Data)
	}
}
