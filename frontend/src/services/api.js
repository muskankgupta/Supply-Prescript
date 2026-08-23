const API_BASE_URL = "http://127.0.0.1:8000";

async function request(endpoint, options = {}) {
    const response = await fetch(
        `${API_BASE_URL}${endpoint}`,
        {
            headers: {
                "Content-Type": "application/json",
                ...(options.headers || {}),
            },
            ...options,
        }
    );

    if (!response.ok) {
        let errorMessage = "API request failed";

        try {
            const error = await response.json();
            errorMessage = error.detail || errorMessage;
        } catch {
            // Ignore JSON parsing error
        }

        throw new Error(errorMessage);
    }

    return response.json();
}


export async function getShipments() {
    return request("/shipments/");
}


export async function getShipment(shipmentId) {
    return request(`/shipments/${shipmentId}`);
}


export async function getPredictions() {
    return request("/predictions/");
}


export async function getPrediction(shipmentId) {
    return request(`/predictions/${shipmentId}`);
}


export async function getRecommendations() {
    return request("/recommendations/");
}


export async function getRecommendationsByShipment(shipmentId) {
    return request(`/recommendations/${shipmentId}`);
}


export async function getDecisions() {
    return request("/decisions/");
}


export async function createDecision(decision) {
    return request("/decisions/", {
        method: "POST",
        body: JSON.stringify(decision),
    });
}