package kafka

import (
	"context"
	"time"

	"github.com/segmentio/kafka-go"
)

type Producer struct{ w *kafka.Writer }

func NewProducer(brokers []string, topic string) *Producer {
	return &Producer{w: &kafka.Writer{
		Addr:         kafka.TCP(brokers...),
		Topic:        topic,
		RequiredAcks: kafka.RequireOne,
	}}
}

func (p *Producer) Send(ctx context.Context, key, value []byte) error {
	return p.w.WriteMessages(ctx, kafka.Message{
		Key:   key,
		Value: value,
		Time:  time.Now(),
	})
}

func (p *Producer) Close() error { return p.w.Close() }

type Consumer struct{ r *kafka.Reader }

func NewConsumer(brokers []string, group, topic string) *Consumer {
	return &Consumer{r: kafka.NewReader(kafka.ReaderConfig{
		Brokers: brokers,
		GroupID: group,
		Topic:   topic,
	})}
}

func (c *Consumer) Fetch(ctx context.Context) (kafka.Message, error) {
	return c.r.FetchMessage(ctx)
}

func (c *Consumer) Commit(ctx context.Context, m kafka.Message) error {
	return c.r.CommitMessages(ctx, m)
}

func (c *Consumer) Close() error { return c.r.Close() }
