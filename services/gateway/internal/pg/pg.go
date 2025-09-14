package pg

import (
	"context"
	"time"

	"github.com/jackc/pgx/v5/pgxpool"
)

type DB struct{ Pool *pgxpool.Pool }

func Connect(ctx context.Context, conn string) (*DB, error) {
	cfg, err := pgxpool.ParseConfig(conn)
	if err != nil {
		return nil, err
	}
	pool, err := pgxpool.NewWithConfig(ctx, cfg)
	if err != nil {
		return nil, err
	}

	ctx2, cancel := context.WithTimeout(ctx, 5*time.Second)
	defer cancel()
	if err := pool.Ping(ctx2); err != nil {
		pool.Close()
		return nil, err
	}

	return &DB{Pool: pool}, nil
}

func (d *DB) Close() { d.Pool.Close() }
