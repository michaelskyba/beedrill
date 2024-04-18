<script>
	import { page, myDecks } from "./store.js";

	async function getDecks() {
		return;

		const response = await fetch("http://127.0.0.1:8000/decks/get/public");
		const data = await response.json();

		const updatedDecks = data.map(deck => {
			return {
				id: deck.deck_id,
				name: deck.deck_name,
				due_cards: deck.due_card_count,
			}
		});
		myDecks.set(updatedDecks);
	}
</script>
