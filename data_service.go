package main

import (
	"errors"

	"github.com/google/uuid"
)

type Movie struct {
	Name        string `json:"name"`
	Link        string `json:"link"`
	TrailerLink string `json:"trailerLink"`
}

type List struct {
	Uuid   string   `json:"uuid"`
	Movies []*Movie `json:"movies"`
}

var lists = []*List{
	{
		Uuid: "Ciao", Movies: []*Movie{
			{Name: "FilmZ", Link: "filmz.com", TrailerLink: "yt.com"},
		},
	},
}

func GetList(uuid string) (*List, error) {
	for _, list := range lists {
		if list.Uuid == uuid {
			return list, nil
		}
	}
	return nil, errors.New("list not found")
}

func GetLists() []*List {
	return lists
}

func CreateList() string {
	uuid := uuid.New().String()
	lists = append(lists, &List{Uuid: uuid, Movies: []*Movie{}})
	return uuid
}

func AddMovie(uuid string, movie Movie) error {
	list, err := GetList(uuid)
	if err != nil {
		return err
	}
	list.Movies = append(list.Movies, &movie)
	return nil
}
