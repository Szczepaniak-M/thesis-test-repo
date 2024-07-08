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

int main() {
    int server_fd, new_socket;
    struct sockaddr_in6 address;
    int addrlen = sizeof(address);
    int buffer, received_value;

    std::srand(std::time(0));
    int random_integer = std::rand() % 100;


    if ((server_fd = socket(AF_INET6, SOCK_STREAM, 0)) == 0) {
        perror("socket failed");
        exit(EXIT_FAILURE);
    }

    address.sin6_family = AF_INET6;
    address.sin6_addr = in6addr_any;
    address.sin6_port = htons(PORT);

    if (bind(server_fd, (struct sockaddr*)&address, sizeof(address)) < 0) {
        perror("bind failed");
        exit(EXIT_FAILURE);
    }

    if (listen(server_fd, 3) < 0) {
        perror("listen");
        exit(EXIT_FAILURE);
    }

    if ((new_socket = accept(server_fd, (struct sockaddr*)&address, (socklen_t*)&addrlen)) < 0) {
        perror("accept");
        exit(EXIT_FAILURE);
    }

    auto start = std::chrono::high_resolution_clock::now();
    send(new_socket, &random_integer, sizeof(random_integer), 0);

    read(new_socket, &buffer, sizeof(buffer));
    received_value = buffer;

    buffer++;
    send(new_socket, &buffer, sizeof(buffer), 0);

    read(new_socket, &buffer, sizeof(buffer));

    auto end = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double, std::milli> elapsed = end - start;

    std::cout << "server" << std::endl;
    std::cout << "Sent random integer: " << random_integer << std::endl;
    std::cout << "Received integer: " << received_value << std::endl;
    std::cout << "Received incremented integer back: " << buffer << std::endl;
    std::cout << "Round-trip time (server-side): " << elapsed.count() << " ms" << std::endl;

    close(new_socket);
    close(server_fd);
    return 0;
}
