export function localizeDate(inputDate) {
	const dateObj = new Date(inputDate);

	// Array of month names in Spanish
	const monthNames = [
		"ene",
		"feb",
		"mar",
		"abr",
		"may",
		"jun",
		"jul",
		"ago",
		"sep",
		"oct",
		"nov",
		"dic",
	];

	// Array of day names in Spanish
	const dayNames = ["Dom", "Lun", "Mar", "Mié", "Jue", "Vie", "Sáb"];

	// Format the date in the desired Argentinian format
	const formattedDate = `${dayNames[dateObj.getUTCDay()]}, ${dateObj.getUTCDate()} ${
		monthNames[dateObj.getUTCMonth()]
	} ${dateObj.getUTCFullYear()} ${dateObj.getUTCHours()}:${dateObj.getUTCMinutes()}:${dateObj.getUTCSeconds()}`;
	return formattedDate;
}
