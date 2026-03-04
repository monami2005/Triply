const API_BASE = '/api';

const api = {
    async get(endpoint) {
        const res = await fetch(`${API_BASE}${endpoint}`);
        return await res.json();
    },
    async post(endpoint, data) {
        const res = await fetch(`${API_BASE}${endpoint}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        return await res.json();
    },
    async put(endpoint, data) {
        const res = await fetch(`${API_BASE}${endpoint}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        return await res.json();
    },
    async delete(endpoint) {
        const res = await fetch(`${API_BASE}${endpoint}`, {
            method: 'DELETE'
        });
        return await res.json();
    },

    // Trips
    getTrips: () => api.get('/trips'),
    getTrip: (id) => api.get(`/trips/${id}`),
    createTrip: (data) => api.post('/trips', data),
    deleteTrip: (id) => api.delete(`/trips/${id}`),

    // Members
    getMembers: (tripId) => api.get(`/trips/${tripId}/members`),
    addMember: (tripId, data) => api.post(`/trips/${tripId}/members`, data),
    updateMember: (id, data) => api.put(`/members/${id}`, data),
    deleteMember: (id) => api.delete(`/members/${id}`),

    // Expenses
    getExpenses: (tripId) => api.get(`/trips/${tripId}/expenses`),
    addExpense: (tripId, data) => api.post(`/trips/${tripId}/expenses`, data),

    // Settings & Templates
    getSettings: () => api.get('/settings'),
    updateSettings: (data) => api.put('/settings', data),
    getTemplates: () => api.get('/templates'),
    saveTemplate: (data) => api.post('/templates', data)
};
