<script>
	import { page, publicDecks, user } from "./store.js";
	import { get } from "svelte/store";

	async function getDecks() {
		const response = await fetch("http://127.0.0.1:8000/decks/get/public");
		const data = await response.json();

		const updatedDecks = data.map(deck => {
			return {
				id: deck.deck_id,
				author: deck.author,
				name: deck.deck_name,
				card_count: deck.card_count,
			}
		}).filter(deck => deck.author != get(user).username);

		publicDecks.set(updatedDecks);
	}

	page.subscribe(v => {
		if (v == "browse_decks")
			getDecks();
	})

	async function cloneDeck(event) {
		const deckId = event.currentTarget.dataset.id;

		const response = await fetch(
			`http://127.0.0.1:8000/decks/${deckId}/clone`,
			{method: "POST"}
		);

		page.set("my_decks");
	}
</script>

{#if $publicDecks.length == 0}
	<p>There are no public decks yet. Maybe you can create one yourself?</p>
{/if}

<div>
	{#each $publicDecks as deck}
		<blockquote>
			<p>
				<strong>{deck.name}</strong> by {deck.author}
			</p>

			<button on:click={cloneDeck} data-id={deck.id}>Clone ({deck.card_count} cards)</button>
		</blockquote>
	{/each}
</div>

<style>
	div {
		display: grid;
		grid-template-columns: 1fr 1fr;
		max-height: 25em;
		overflow-y: scroll;
	}

	blockquote {
		margin: 1em;
	}

	button {
		margin-top: 2em;
	}
</style>
