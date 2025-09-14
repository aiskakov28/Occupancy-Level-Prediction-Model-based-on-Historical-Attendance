package redis

import (
	goredis "github.com/redis/go-redis/v9"
)

func New(addr, password string, db int) *goredis.Client {
	return goredis.NewClient(&goredis.Options{
		Addr:     addr,
		Password: password,
		DB:       db,
	})
}
