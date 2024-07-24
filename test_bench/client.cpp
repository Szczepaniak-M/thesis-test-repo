#include <iostream>
#include <cstdlib>
#include <ctime>
#include <cstring>
#include <unistd.h>
#include <netdb.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <chrono>

#define PORT 8080

int main(int argc, char *argv[]) {
    if (argc != 2) {
        std::cerr << "Usage: " << argv[0] << " <hostname>" << std::endl;
        return 1;
    }

    sleep(5); // ensure server works
    const char *hostname = argv[1];
    struct addrinfo hints, *res;
    int sock = 0;
    int buffer, received_value;

    std::srand(std::time(0));
    int random_integer = std::rand() % 100;

    memset(&hints, 0, sizeof(hints));
    hints.ai_family = AF_INET6;
    hints.ai_socktype = SOCK_STREAM;

    int status = getaddrinfo(hostname, nullptr, &hints, &res);
    if (status != 0) {
        std::cerr << "getaddrinfo error: " << gai_strerror(status) << std::endl;
        return 1;
    }

    if ((sock = socket(res->ai_family, res->ai_socktype, res->ai_protocol)) < 0) {
        std::cerr << "Socket creation error" << std::endl;
        freeaddrinfo(res);
        return -1;
    }

    ((struct sockaddr_in6 *)res->ai_addr)->sin6_port = htons(PORT);

    if (connect(sock, res->ai_addr, res->ai_addrlen) < 0) {
        std::cerr << "Connection Failed" << std::endl;
        close(sock);
        freeaddrinfo(res);
        return -1;
    }

    freeaddrinfo(res);
    std::cout << "Client" << std::endl;
    for(int i = 0; i < 11; i++) {
        auto start = std::chrono::high_resolution_clock::now();
        send(sock, &random_integer, sizeof(random_integer), 0);

        read(sock, &buffer, sizeof(buffer));
        received_value = buffer;

        buffer++;
        send(sock, &buffer, sizeof(buffer), 0);

        read(sock, &buffer, sizeof(buffer));

        auto end = std::chrono::high_resolution_clock::now();
        std::chrono::duration<double, std::milli> elapsed = end - start;
        std::cout << "Round-trip time: " << elapsed.count() << " ms" << std::endl;
    }

    close(sock);
    return 0;
}
