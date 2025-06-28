package com.banco.verifyemailservice;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.mail.SimpleMailMessage;
import org.springframework.mail.javamail.JavaMailSender;
import org.springframework.stereotype.Service;

@Service
public class EmailService {

    @Autowired
    private JavaMailSender mailSender;

    public void sendVerificationEmail(String to, String token) {
        String link = "http://localhost:8084/verify-email/confirm?token=" + token;
        String subject = "Verifica tu correo electrónico";
        String content = "Hola,\n\nPara confirmar tu dirección de correo electrónico, haz clic en el siguiente enlace:\n"
                + link + "\n\nGracias.";

        SimpleMailMessage message = new SimpleMailMessage();
        message.setTo(to);
        message.setSubject(subject);
        message.setText(content);
        mailSender.send(message);
    }
}

