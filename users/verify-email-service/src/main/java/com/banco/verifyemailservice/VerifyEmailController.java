package com.banco.verifyemailservice;


import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/verify")
public class VerifyEmailController {

    @Autowired
    private GmailService gmailService;

    @PostMapping("/send")
    public String sendVerificationEmail(@RequestParam String toEmail) {
        try {
            gmailService.sendEmail(
                toEmail,
                "Verifica tu cuenta",
                "Hola, por favor haz clic en el siguiente enlace para verificar tu cuenta."
            );
            return "Correo enviado correctamente a " + toEmail;
        } catch (Exception e) {
            return "Error al enviar correo: " + e.getMessage();
        }
    }
}
