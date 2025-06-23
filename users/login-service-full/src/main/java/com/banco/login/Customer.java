package com.banco.login;
import jakarta.persistence.*;
import java.time.LocalDateTime;

@Entity
@Table(name = "customers")
public class Customer {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private int id_users;
    private String name;
    private String lastname;
    private String mail;
    private String hashPassword;
    private String phone;
    private String documentId;
    private LocalDateTime registrationDate;
    private String state;

    public int getId_users() { return id_users; }
    public void setId_users(int id) { this.id_users = id; }
    public String getMail() { return mail; }
    public void setMail(String mail) { this.mail = mail; }
    public String getHashPassword() { return hashPassword; }
    public void setHashPassword(String pwd) { this.hashPassword = pwd; }
}
