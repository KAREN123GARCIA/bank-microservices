package com.banco.resetpasswordservice;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.web.bind.annotation.*;

import java.util.Optional;

@RestController
@RequestMapping("/reset-password")
public class controller {

    @Autowired
    private repository repo;

    @Autowired
    private BCryptPasswordEncoder passwordEncoder;

    @PutMapping("/{email}")
    public ResponseEntity<?> resetPassword(
            @PathVariable String email,
            @RequestBody ResetPasswordRequest body
    ) {
        String normalizedMail = email.trim().toLowerCase();
        Optional<entity> found = repo.findByMail(normalizedMail);

        if (found.isPresent()) {
            entity user = found.get();

            // Validar contraseña antigua
            if (!passwordEncoder.matches(body.getOldPassword(), user.getHashPassword())) {
                return ResponseEntity.status(401).body("❌ Contraseña antigua incorrecta");
            }

            // Hashear nueva contraseña
            String hashedNewPassword = passwordEncoder.encode(body.getNewPassword());
            user.setHashPassword(hashedNewPassword);

            repo.save(user);

            System.out.println("✅ Contraseña cambiada correctamente para: " + normalizedMail);
            return ResponseEntity.ok("Contraseña actualizada correctamente");
        } else {
            return ResponseEntity.status(404).body("Usuario no encontrado");
        }
    }
}
