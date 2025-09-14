package csv

import (
	"bufio"
	"context"
	"encoding/csv"
	"os"
	"strconv"
	"strings"
	"time"
)

type Event struct {
	TS       time.Time `json:"ts"`
	Count    int       `json:"count"`
	DeviceID string    `json:"device_id"`
	Source   string    `json:"source"`
}

func Stream(ctx context.Context, path string, speed float64, device string) (<-chan Event, error) {
	f, err := os.Open(path)
	if err != nil {
		return nil, err
	}
	r := csv.NewReader(bufio.NewReader(f))
	r.FieldsPerRecord = -1
	out := make(chan Event, 128)

	go func() {
		defer close(out)
		defer f.Close()
		header := true
		var lastTS *time.Time
		for {
			rec, err := r.Read()
			if err != nil {
				return
			}
			if header {
				header = false
				continue
			}
			if len(rec) < 3 {
				continue
			}
			ts, err := time.ParseInLocation(
				"2006-01-02 15:04",
				strings.TrimSpace(rec[0])+" "+strings.TrimSpace(rec[1]),
				time.Local,
			)
			if err != nil {
				continue
			}
			cnt, err := strconv.Atoi(strings.TrimSpace(rec[2]))
			if err != nil {
				continue
			}
			if lastTS != nil && speed > 0 {
				d := ts.Sub(*lastTS)
				if d > 0 {
					time.Sleep(time.Duration(float64(d) / speed))
				}
			}
			v := Event{TS: ts.UTC(), Count: cnt, DeviceID: device, Source: "csv"}
			select {
			case <-ctx.Done():
				return
			case out <- v:
			}
			lastTS = &ts
		}
	}()
	return out, nil
}
