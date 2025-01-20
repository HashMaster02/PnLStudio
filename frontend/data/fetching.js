export const fetchCardData = async (filterData) => {
    try {
        const response = await fetch('http://localhost:8000/api/card-data', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(filterData),
        });
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error fetching card data:', error);
        return null;
    }
};

export const fetchGraphData = async (filterData) => {
    try {
        const response = await fetch('http://localhost:8000/api/graph-data', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(filterData),
        });
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error fetching graph data:', error);
        return null;
    }
};

export const fetchTopDownBottomUpData = async (filterData) => {
    try {
        const response = await fetch(
            'http://localhost:8000/api/top-down-bottom-up',
            {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(filterData),
            }
        );
        const data = await response.json();
        return data;
    } catch (error) {
        console.error(
            'Error fetching top-down and bottom-up securities data:',
            error
        );
        return null;
    }
};

export const fetchAccountsData = async () => {
    try {
        const response = await fetch('http://localhost:8000/api/accounts', {
            method: 'GET',
        });
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error fetching security tickers data:', error);
        return null;
    }
};

export const fetchSecuritiesData = async () => {
    try {
        const response = await fetch(
            'http://localhost:8000/api/security-tickers',
            {
                method: 'GET',
            }
        );
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error fetching accounts data:', error);
        return null;
    }
};
