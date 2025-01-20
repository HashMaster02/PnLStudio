export const refreshDb = async () => {
	try {
		const response = await fetch(
			'http://localhost:8000/api/database/refresh',
			{
				method: 'GET',
			}
		);
		const data = await response.json();
		return data;
	} catch (error) {
		console.error('Error fetching card data:', error);
		return null;
	}
};
