const RECIPIENT = 'horizonarkstudio@gmail.com';

export const feedbackSubjects = [
	'Feedback on the writing',
	'Feedback on the website',
	'Feedback on a paperback',
	'Feedback about the author'
] as const;

// Ported 1:1 from the original script.js feedback-form handler:
// builds a mailto: link and hands off to the user's email app.
// No server, no data collection — same as before.
export function useFeedbackForm() {
	let subject = $state<string>(feedbackSubjects[0]);
	let name = $state('');
	let message = $state('');

	function submit() {
		const body = (name.trim() ? `From: ${name.trim()}\n\n` : '') + message.trim();
		const mailto = `mailto:${RECIPIENT}?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
		window.location.href = mailto;
	}

	return {
		get subject() {
			return subject;
		},
		set subject(value: string) {
			subject = value;
		},
		get name() {
			return name;
		},
		set name(value: string) {
			name = value;
		},
		get message() {
			return message;
		},
		set message(value: string) {
			message = value;
		},
		submit,
		recipient: RECIPIENT
	};
}
