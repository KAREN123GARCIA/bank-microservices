package main

import (
    "fmt"
    "log"
    "net/http"
    "github.com/gorilla/websocket"
)

var upgrader = websocket.Upgrader{
    CheckOrigin: func(r *http.Request) bool { return true },
}

type SmsMessage struct {
    Phone string `json:"phone"`
    Body  string `json:"body"`
}

func sendSMS(phone, body string) {
    log.Printf("📱 SMS enviado a %s: %s", phone, body)
}

func smsHandler(w http.ResponseWriter, r *http.Request) {
    conn, err := upgrader.Upgrade(w, r, nil)
    if err != nil {
        log.Println("Error al hacer upgrade:", err)
        return
    }
    defer conn.Close()

    for {
        var msg SmsMessage
        err := conn.ReadJSON(&msg)
        if err != nil {
            log.Println("Error al leer mensaje:", err)
            break
        }
        sendSMS(msg.Phone, msg.Body)
        response := fmt.Sprintf("✅ SMS a %s fue enviado exitosamente", msg.Phone)
        conn.WriteMessage(websocket.TextMessage, []byte(response))
    }
}

func main() {
    http.HandleFunc("/ws/sms", smsHandler)
    fmt.Println("📱 Servicio WebSocket de envío de SMS corriendo en :8096/ws/sms")
    log.Fatal(http.ListenAndServe(":8096", nil))
}