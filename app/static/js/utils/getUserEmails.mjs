export async function getUserEmails(user_id, skip = 0, limit = 3) {
	const url =
		`/users/${user_id}/emails/?` +
		new URLSearchParams({
			skip: skip,
			limit: limit,
		});
	try {
		const response = await fetch(url, {
			method: "GET",
			headers: {
				"Content-Type": "application/json",
			},
		});

		if (!response.ok) {
			throw new Error(`Failed to retrieve user emails. Status code: ${response.status}`);
		}

		const emails = await response.json();
		console.log(`For the user with the id ${user_id}, got the following emails:`);
		console.dir(emails);
		return emails;
	} catch (error) {
		console.error(error);
	}
}
