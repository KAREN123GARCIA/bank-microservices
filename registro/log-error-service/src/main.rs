
use actix_web::{post, web, App, HttpServer, Responder, HttpResponse};
use redis::{AsyncCommands, Client};
use serde::Deserialize;
use serde_json::json;

#[derive(Deserialize)]
struct LogEntry {
    service: String,
    level: String,
    message: String,
}

#[post("/log-error")]
async fn log_error(
    data: web::Json<LogEntry>,
    redis: web::Data<Client>,
) -> impl Responder {
    let mut con = redis.get_async_connection().await.unwrap();
    let key = format!("error:{}:{}", data.service, chrono::Utc::now().timestamp());
    let value = json!({
        "level": data.level,
        "message": data.message
    })
    .to_string();

    let result: redis::RedisResult<()> = con.set(&key, value).await;

    match result {
        Ok(_) => HttpResponse::Ok().json(json!({ "message": "Error registrado correctamente" })),
        Err(_) => HttpResponse::InternalServerError().json(json!({ "error": "Fallo al registrar el error" })),
    }
}

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    let redis_url = "redis://redis:6379";
    let client = Client::open(redis_url).expect("No se pudo conectar a Redis");

    HttpServer::new(move || {
        App::new()
            .app_data(web::Data::new(client.clone()))
            .service(log_error)
    })
    .bind("0.0.0.0:8100")?
    .run()
    .await
}
