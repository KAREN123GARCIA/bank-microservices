package main

import (
	"fmt"
	"log"
	"net/http"

	"github.com/gorilla/websocket"
)

var upgrader = websocket.Upgrader{
	CheckOrigin: func(r *http.Request) bool {
		return true // 🔓 Permite conexiones desde cualquier origen (incluye file:// y localhost)
	},
}

type EmailMessage struct {
	To      string `json:"to"`
	Subject string `json:"subject"`
	Body    string `json:"body"`
}

func sendEmail(to, subject, body string) {
	log.Printf("📧 Email enviado a %s con asunto: %s\nContenido: %s", to, subject, body)
}

func emailHandler(w http.ResponseWriter, r *http.Request) {
	conn, err := upgrader.Upgrade(w, r, nil)
	if err != nil {
		log.Println("Error al hacer upgrade:", err)
		return
	}
	defer conn.Close()

	for {
		var msg EmailMessage
		err := conn.ReadJSON(&msg)
		if err != nil {
			log.Println("Error al leer mensaje:", err)
			break
		}
		sendEmail(msg.To, msg.Subject, msg.Body)
		response := fmt.Sprintf("✅ Email a %s fue enviado exitosamente", msg.To)
		conn.WriteMessage(websocket.TextMessage, []byte(response))
	}
}

func main() {
	http.HandleFunc("/ws/email", emailHandler)
	fmt.Println("🚀 Servicio WebSocket de envío de correos corriendo en :8095/ws/email")
	log.Fatal(http.ListenAndServe(":8095", nil))
}
