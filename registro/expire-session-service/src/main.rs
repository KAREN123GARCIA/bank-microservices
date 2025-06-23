use actix_web::{delete, web, App, HttpServer, Responder, HttpResponse};
use redis::{AsyncCommands, Client};
use serde_json::json;

#[delete("/session/{id}")]
async fn expire_session(
    path: web::Path<String>,
    redis: web::Data<Client>,
) -> impl Responder {
    let session_id = path.into_inner();
    let mut con = redis.get_async_connection().await.unwrap();
    let result: redis::RedisResult<()> = con.del(&session_id).await;

    match result {
        Ok(_) => HttpResponse::Ok().json(json!({ "message": "Sesión expirada correctamente" })),
        Err(_) => HttpResponse::InternalServerError().json(json!({ "error": "No se pudo expirar la sesión" })),
    }
}

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    let redis_url = "redis://redis:6379";
    let client = Client::open(redis_url).expect("No se pudo conectar a Redis");

    HttpServer::new(move || {
        App::new()
            .app_data(web::Data::new(client.clone()))
            .service(expire_session)
    })
    .bind("0.0.0.0:8099")?
    .run()
    .await
}
