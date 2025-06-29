use async_graphql::{Schema, EmptyMutation, EmptySubscription, Object, Request as GraphQLRequest, Response as GraphQLResponse};
use axum::{routing::post, Router, extract::{State, Json}};
use tokio::net::TcpListener;

struct QueryRoot;

#[Object]
impl QueryRoot {
    async fn verify_session(&self, token: String) -> bool {
        // Aquí deberías verificar el token en Redis
        token == "valid-session-token"
    }
}

#[tokio::main]
async fn main() {
    let schema = Schema::build(QueryRoot, EmptyMutation, EmptySubscription).finish();

    let app = Router::new()
        .route("/graphql", post(graphql_handler))
        .with_state(schema);

    let listener = TcpListener::bind("0.0.0.0:8097").await.unwrap();
    println!("🚀 Running GraphQL verify-session-service on http://0.0.0.0:8097");
    axum::serve(listener, app).await.unwrap();
}

async fn graphql_handler(
    State(schema): State<Schema<QueryRoot, EmptyMutation, EmptySubscription>>,
    Json(req): Json<GraphQLRequest>,
) -> Json<GraphQLResponse> {
    let resp = schema.execute(req).await;
    Json(resp)
}