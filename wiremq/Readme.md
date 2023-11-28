# WireMQ Examples

This directory contains several example tests with simple applications 
running WireMQ.

## Installing WireMQ

Pre-requisites: 
- Python 3.9 or later
- Pip

It is recommended to install the requirements and WireMQ in a virtual environment.

To install the requirements run:

`pip install -r requirements.txt`

To install wiremq run:

`pip install wiremq-0.0.1-py3-none-any.whl`

## Test descriptions

### test_bus

Three bus endpoints are set up. Bus endpoints always send messages to all other members of the bus network.

Each bus is selective in its consumption and discards messages not addressed to it.

In this test, bus1 sends messages to bus2, bus2 to bus3 and bus3 to bus1.

```
              msg                msg
          ┌──────────┐       ┌─────────┐
          │          │       │         │
 ┌────────┴──┐     ┌─▼───────┴─┐     ┌─▼─────────┐
 │ bus1      │     │ bus2      │     │ bus3      │
 │ 127.0.0.1 │     │ 127.0.0.1 │     │ 127.0.0.1 │
 │ 9001      │     │ 9002      │     │ 9003      │
 └────────▲──┘     └───────────┘     └─┬─────────┘
          │                            │
          └────────────────────────────┘
                       msg
```

### test_channel

Two channels are initialised and channel 2 sends messages to channel 1.

Channels are intended for P2P connections and each has one pre-configured destination.

```
 ┌───────────┐            ┌───────────┐
 │ channel1  │            │ channel2  │
 │ 127.0.0.1 ◄─────msg────┤ 127.0.0.1 │
 │ 10000     │            │ 10001     │
 └───────────┘            └───────────┘

```

### test_pubsub

A pubsub channel sends notifications to two subscribed channels.

Channel 2 is pre-subscribed to the pubsub and receives event notifications immediately.

Channel 1 is initially not subscribed, but sends a command message containing a subscription payload. After the pubsub receives the command message, channel 1 starts receiving event notifications

```
                               ┌───────────┐
                               │ channel1  │
         ┌───────event msg─────► 127.0.0.1 │
         │                     │ 8803      │
┌────────┴───────┐             └───────────┘
│ pubsub1        │
│ 127.0.0.1      │
│ 8801 (event)   ◄──────cmd msg───┐
│ 8802 (command) │                │
└────────┬───────┘             ┌──┴────────┐
         │                     │ channel2  │
         └───────event msg─────► 127.0.0.1 │
                               │ 8804      │
                               └───────────┘
```

### test_router

A router is set up with the following routing table:

```
127.0.0.1:8901 -> 127.0.0.1: 8902
127.0.0.1:8902 -> 127.0.0.1: 8901
```

Channel 2 sends messages to the router. The messages contain channel 2's host and port number in the headers.

The router automatically reads these headers and routes the message to channel 1.

```
 ┌───────────┐          ┌───────────┐          ┌───────────┐
 │ channel1  │          │ router    │          │ channel2  │
 │ 127.0.0.1 ◄────msg───┤ 127.0.0.1 ◄────msg───┤ 127.0.0.1 │
 │ 8901      │          │ 8900      │          │ 8902      │
 └───────────┘          └───────────┘          └───────────┘
```

### test_serviceactivator

The service activator test comprises of:

- A main application which contains a service activator, and bus 0 which
  aggregates the service messages
- Two HTTP clients, one calls the `cpu/get_percent`` path, the other calls 
  the `ram/get_available`` path
- Two more bus endpoints which each supply the raw data to respond to the
  serviceactivator via bus0.


```

 ┌───────────────────┐     8000
 │ HTTP client 1     ├─────GET───────┐
 │ GET               │               │
 │ cpu/get_percent   │               │
 └──────────────▲────┘             ┌─▼────────────────┐              ┌───────────┐
                └─────response─────┤ serviceactivator ├───wmq msg────► bus0      │
                                   │ 127.0.0.1        │              │ 127.0.0.1 │
                                   │ 8000 (HTTP)      ◄───wmq msg────┤ 9010      ├────┐
                ┌─────response─────┤ 11000 (wiremq)   │              └▲───┬─────▲┘    │
 ┌──────────────▼────┐             └─▲────────────────┘               │   │     │    wmq
 │ HTTP client 2     │               │                                │  wmq    │    msg
 │ GET               │     8000      │                               res msg   res   RAM
 │ ram/get_available ├─────GET───────┘                                │  CPU    │     │
 └───────────────────┘                                     ┌──────────┴┐  │    ┌┴─────▼────┐
                                                           │ bus1      │  │    │ bus2      │
                                                           │ 127.0.0.1 ◄──┘    │ 127.0.0.1 │
                                                           │ 9011      │       │ 9012      │
                                                           └───────────┘       └───────────┘
```