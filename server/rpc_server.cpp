#include <iostream>
#include <cmath>
#include <algorithm>
#include <thread>
#include <chrono>

#include "SimplePocoHandler.h"

bool is_prime(int64_t x){
    int64_t right = sqrt(x);
    for(int64_t i=2;i<=right;i++)
        if(x%i==0) return false;
    return true;
}

int64_t nearest_prime(int64_t n)
{
    if (n < 3) 
        return 2;
    if (is_prime(n)) 
        return n;

    int64_t candidate;
    int64_t delta = 2 - (n % 2 == 0);
    while (true){
       for (int i=-1; i<2; i+=2){
          candidate = n + delta*i;
          if (is_prime(candidate)) {return candidate;}
       }
       delta += 2;
    }
}

int main(void)
{
    SimplePocoHandler handler("rabbitmq", 5672);

    AMQP::Connection connection(&handler, AMQP::Login("guest", "guest"), "/");

    AMQP::Channel channel(&connection);
    channel.setQos(1);

    channel.declareQueue("nearest_prime");
    channel.consume("").onReceived([&channel](const AMQP::Message &message,
            uint64_t deliveryTag,
            bool redelivered)
    {
        const auto body = message.message();
        std::cout<<" [.] nearest_prime("<<body<<")"<<std::endl;

        AMQP::Envelope env(std::to_string(nearest_prime(std::stoi(body))));
        env.setCorrelationID(message.correlationID());

        channel.publish("", message.replyTo(), env);
        channel.ack(deliveryTag);
    });

    std::cout << " [x] Awaiting RPC requests" << std::endl;
    handler.loop();
    return 0;
}
