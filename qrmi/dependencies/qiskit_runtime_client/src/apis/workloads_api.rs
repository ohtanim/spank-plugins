/*
 * Qiskit Runtime API
 *
 * The Qiskit Runtime API description
 *
 * The version of the OpenAPI document: 0.21.2
 *
 * Generated by: https://openapi-generator.tech
 */

use super::{configuration, ContentType, Error};
use crate::{apis::ResponseContent, models};
use reqwest;
use serde::{de::Error as _, Deserialize, Serialize};

/// struct for typed errors of method [`find_instance_workloads`]
#[derive(Debug, Clone, Serialize, Deserialize)]
#[serde(untagged)]
pub enum FindInstanceWorkloadsError {
    Status401(models::FindInstanceWorkloads401Response),
    UnknownValue(serde_json::Value),
}

/// List user instance workloads
pub async fn find_instance_workloads(
    configuration: &configuration::Configuration,
    ibm_api_version: Option<&str>,
    sort: Option<&str>,
    limit: Option<f64>,
    previous: Option<&str>,
    next: Option<&str>,
    backend: Option<&str>,
    search: Option<&str>,
    status: Option<Vec<String>>,
    mode: Option<&str>,
    created_after: Option<String>,
    created_before: Option<String>,
    tags: Option<Vec<String>>,
) -> Result<models::FindInstanceWorkloads200Response, Error<FindInstanceWorkloadsError>> {
    // add a prefix to parameters to efficiently prevent name collisions
    let p_ibm_api_version = ibm_api_version;
    let p_sort = sort;
    let p_limit = limit;
    let p_previous = previous;
    let p_next = next;
    let p_backend = backend;
    let p_search = search;
    let p_status = status;
    let p_mode = mode;
    let p_created_after = created_after;
    let p_created_before = created_before;
    let p_tags = tags;

    let uri_str = format!("{}/workloads", configuration.base_path);
    let mut req_builder = configuration.client.request(reqwest::Method::GET, &uri_str);

    if let Some(ref param_value) = p_sort {
        req_builder = req_builder.query(&[("sort", &param_value.to_string())]);
    }
    if let Some(ref param_value) = p_limit {
        req_builder = req_builder.query(&[("limit", &param_value.to_string())]);
    }
    if let Some(ref param_value) = p_previous {
        req_builder = req_builder.query(&[("previous", &param_value.to_string())]);
    }
    if let Some(ref param_value) = p_next {
        req_builder = req_builder.query(&[("next", &param_value.to_string())]);
    }
    if let Some(ref param_value) = p_backend {
        req_builder = req_builder.query(&[("backend", &param_value.to_string())]);
    }
    if let Some(ref param_value) = p_search {
        req_builder = req_builder.query(&[("search", &param_value.to_string())]);
    }
    if let Some(ref param_value) = p_status {
        req_builder = match "multi" {
            "multi" => req_builder.query(
                &param_value
                    .iter()
                    .map(|p| ("status".to_owned(), p.to_string()))
                    .collect::<Vec<(std::string::String, std::string::String)>>(),
            ),
            _ => req_builder.query(&[(
                "status",
                &param_value
                    .iter()
                    .map(|p| p.to_string())
                    .collect::<Vec<String>>()
                    .join(",")
                    .to_string(),
            )]),
        };
    }
    if let Some(ref param_value) = p_mode {
        req_builder = req_builder.query(&[("mode", &param_value.to_string())]);
    }
    if let Some(ref param_value) = p_created_after {
        req_builder = req_builder.query(&[("created_after", &param_value.to_string())]);
    }
    if let Some(ref param_value) = p_created_before {
        req_builder = req_builder.query(&[("created_before", &param_value.to_string())]);
    }
    if let Some(ref param_value) = p_tags {
        req_builder = match "multi" {
            "multi" => req_builder.query(
                &param_value
                    .iter()
                    .map(|p| ("tags".to_owned(), p.to_string()))
                    .collect::<Vec<(std::string::String, std::string::String)>>(),
            ),
            _ => req_builder.query(&[(
                "tags",
                &param_value
                    .iter()
                    .map(|p| p.to_string())
                    .collect::<Vec<String>>()
                    .join(",")
                    .to_string(),
            )]),
        };
    }
    if let Some(ref user_agent) = configuration.user_agent {
        req_builder = req_builder.header(reqwest::header::USER_AGENT, user_agent.clone());
    }
    if let Some(param_value) = p_ibm_api_version {
        req_builder = req_builder.header("IBM-API-Version", param_value.to_string());
    }
    if let Some(ref token) = configuration.bearer_access_token {
        req_builder = req_builder.bearer_auth(token.to_owned());
    };
    if let Some(ref crn) = configuration.crn {
        req_builder = req_builder.header("Service-CRN", crn.clone());
    }
    req_builder = req_builder.header(reqwest::header::ACCEPT, "application/json");

    let req = req_builder.build()?;
    let resp = configuration.client.execute(req).await?;

    let status = resp.status();
    let content_type = resp
        .headers()
        .get("content-type")
        .and_then(|v| v.to_str().ok())
        .unwrap_or("application/json");
    let content_type = super::ContentType::from(content_type);

    if !status.is_client_error() && !status.is_server_error() {
        let content = resp.text().await?;
        match content_type {
            ContentType::Json => serde_json::from_str(&content).map_err(Error::from),
            ContentType::Text => Err(Error::from(serde_json::Error::custom("Received `text/plain` content type response that cannot be converted to `models::FindInstanceWorkloads200Response`"))),
            ContentType::Unsupported(unknown_type) => Err(Error::from(serde_json::Error::custom(format!("Received `{unknown_type}` content type response that cannot be converted to `models::FindInstanceWorkloads200Response`")))),
        }
    } else {
        let content = resp.text().await?;
        let entity: Option<FindInstanceWorkloadsError> = serde_json::from_str(&content).ok();
        Err(Error::ResponseError(ResponseContent {
            status,
            content,
            entity,
        }))
    }
}
