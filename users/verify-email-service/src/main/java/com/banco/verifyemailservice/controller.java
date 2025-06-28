package com.banco.verifyemailservice;
import java.util.UUID;
import java.time.LocalDateTime;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/verify-email")
public class controller {

    @Autowired
    private EmailService emailService;

    @Autowired
    private VerificationTokenRepository tokenRepo;

    @PostMapping
    public ResponseEntity<?> solicitarVerificacion(@RequestParam String email) {
        String normalized = email.trim().toLowerCase();
        String token = UUID.randomUUID().toString();

        VerificationToken vt = new VerificationToken();
        vt.setEmail(normalized);
        vt.setToken(token);
        vt.setCreatedAt(LocalDateTime.now());
        vt.setExpiresAt(LocalDateTime.now().plusMinutes(10));
        vt.setVerified(false);

        tokenRepo.save(vt);
        emailService.sendVerificationEmail(normalized, token);

        return ResponseEntity.ok("Se ha enviado un correo de verificación a " + email);
    }
}
