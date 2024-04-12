package main

import (
	"net/http"

	"github.com/gin-gonic/gin"
)

func main() {
	router := gin.Default()
	router.GET("/lists", getLists)
	router.POST("/lists", createList)
	router.GET("/lists/:uuid/movies", getList)

	router.POST("/lists/:uuid/movies", func(c *gin.Context) {
		var requestBody Movie

		if err := c.BindJSON(&requestBody); err != nil {
			c.IndentedJSON(http.StatusBadRequest, "the request body isn't in the right format")
			return
		}
		err := AddMovie(c.Param("uuid"), requestBody)
		if err != nil {
			c.IndentedJSON(http.StatusNotFound, err)
		}
		c.IndentedJSON(http.StatusCreated, "New Movie added.")

	})

	router.Run("localhost:8000")
}

func getList(c *gin.Context) {
	p, err := GetList(c.Param("uuid"))
	if err != nil {
		c.IndentedJSON(http.StatusNotFound, err)
		return
	}
	list := *p
	c.IndentedJSON(http.StatusOK, list.Movies)
}
func getLists(c *gin.Context) {
	lists = GetLists()
	c.IndentedJSON(http.StatusOK, lists)
}

func createList(c *gin.Context) {
	uuid := CreateList()
	c.IndentedJSON(http.StatusCreated, uuid)
}
