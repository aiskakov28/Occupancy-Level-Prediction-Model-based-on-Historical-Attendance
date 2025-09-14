package main

import (
	"context"
	"encoding/json"
	"flag"
	"log"
	"os"
	"strings"
	"time"

	csvsrc "occupancy/ingest/internal/sources/csv"
	iotsrc "occupancy/ingest/internal/sources/iot_http"

	"github.com/segmentio/kafka-go"
)

func writer(brokers, topic string) *kafka.Writer {
	return &kafka.Writer{
		Addr:         kafka.TCP(strings.Split(brokers, ",")...),
		Topic:        topic,
		Balancer:     &kafka.LeastBytes{},
		RequiredAcks: kafka.RequireOne,
	}
}

func main() {
	mode := flag.String("mode", "csv", "csv|http")
	brokers := flag.String("kafka", os.Getenv("KAFKA_BROKERS"), "host1:9092,host2:9092")
	topic := flag.String("topic", "occupancy.events", "kafka topic")
	csvPath := flag.String("csv", "../../dbt_occupancy/seeds/gym_dataset.csv", "path to csv")
	speed := flag.Float64("speed", 60, "time acceleration (csv)")
	device := flag.String("device", "sensor-1", "device id (csv)")
	addr := flag.String("addr", ":8085", "http listen addr (http)")
	flag.Parse()

	ctx := context.Background()
	w := writer(*brokers, *topic)
	defer w.Close()

	switch *mode {
	case "csv":
		ch, err := csvsrc.Stream(ctx, *csvPath, *speed, *device)
		if err != nil {
			log.Fatal(err)
		}
		for e := range ch {
			buf, _ := json.Marshal(e)
			if err := w.WriteMessages(ctx, kafka.Message{Value: buf, Time: time.Now()}); err != nil {
				log.Println("kafka write:", err)
			}
		}
	case "http":
		ch := iotsrc.Start(ctx, *addr)
		log.Println("listening on", *addr)
		for e := range ch {
			buf, _ := json.Marshal(e)
			if err := w.WriteMessages(ctx, kafka.Message{Value: buf, Time: time.Now()}); err != nil {
				log.Println("kafka write:", err)
			}
		}
	default:
		log.Fatal("unknown mode")
	}
}
