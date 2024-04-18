<script>
	import { page, editingDeck } from "./store.js";
	import { get } from "svelte/store";

	let front;
	let back;

	let cards = [];

	async function getCards() {
		const deckId = get(editingDeck).id;
		const response = await fetch(`http://127.0.0.1:8000/decks/${deckId}/get_all`);
		cards = await response.json();
	}

	page.subscribe(v => {
		if (v == "edit_deck")
			getCards();
	});

	async function createCard() {
		const response = await fetch("http://127.0.0.1:8000/cards/add", {
			method: "POST",
			headers: {
				"Content-Type": "application/json",
			},
			body: JSON.stringify({
				deck_id: get(editingDeck).id,
				front: front,
				back: back,
			}),
		});

		front = "";
		back = "";

		const data = await response.json();
		getCards();
	}

	async function deleteCard(event) {
		const cardId = event.currentTarget.dataset.id;

		const response = await fetch(`http://127.0.0.1:8000/cards/${cardId}/delete`, {
			method: "DELETE",
		});

		const data = await response.json();
		getCards();
	}
</script>

{#if cards.length == 0}
	<p>{$editingDeck.name} has no cards yet.</p>
{:else}
	<p>{$editingDeck.name} has {cards.length} cards.</p>
{/if}

<input placeholder="Front" bind:value={front}>
<input placeholder="Back" bind:value={back}>
<button on:click={createCard}>Add</button>

{#if cards.length > 0}
	{#each cards as card}
		<blockquote>
			<p>{card.front}</p>
			<hr>
			<p>{card.back}</p>
			<hr class="half">

			<button on:click={deleteCard} data-id={card.card_id}>Delete</button>
		</blockquote>
	{/each}
{/if}

<style>
	hr.half {
		width: 25%;
		margin-left: 0;
	}
</style>
