package com.banco.resetpasswordservice;
import jakarta.persistence.*;

@Entity
@Table(name = "customers")
public class entity {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private int id_users;
    private String mail;
    private String hashPassword;

    public String getMail() { return mail; }
    public void setMail(String mail) { this.mail = mail; }
    public String getHashPassword() { return hashPassword; }
    public void setHashPassword(String hashPassword) { this.hashPassword = hashPassword; }
}