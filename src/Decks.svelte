<script>
	import { page, myDecks } from "./store.js";

	let deckName;

	async function getDecks() {
		const response = await fetch("http://127.0.0.1:8000/decks/get/mine");
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

	page.subscribe(v => {
		if (v == "my_decks")
			getDecks();
	})

	async function newDeck(type) {
		if (!deckName)
			return;

		const isPublic = type == "public" ? 1 : 0;

		const response = await fetch("http://127.0.0.1:8000/decks/new", {
			method: "POST",
			headers: {
				"Content-Type": "application/json",
			},
			body: JSON.stringify({
				name: deckName,
				public: isPublic,
			}),
		});

		deckName = "";

		const data = await response.json();
		console.log(data);

		getDecks();
	}

	async function deleteDeck(event) {
		const response = await fetch("http://127.0.0.1:8000/decks/delete", {
			method: "POST",
			headers: {
				"Content-Type": "application/json",
			},
			body: JSON.stringify({
				deck_id: event.currentTarget.dataset.id,
			}),
		});

		getDecks();
	}
</script>

{#if $myDecks.length == 0}
	<p>You have no decks yet. Create one yourself or import a public deck!</p>
{/if}

<div>
	{#each $myDecks as deck}
		<blockquote>
			<strong>{deck.name}</strong>
			<hr>

			{#if deck.due_cards == 0}
				<p>There are no due cards.</p>
				<button disabled>Review</button>
			{:else}
				<p>Due cards: <span class="due">{deck.due_cards}</span></p>
				<button>Review</button>
			{/if}

			<button>Edit</button>
			<button on:click={deleteDeck} data-id={deck.id}>Delete</button>
		</blockquote>
	{/each}
</div>

<hr>

<input placeholder="Deck name" bind:value={deckName}>
<button on:click={() => newDeck("public")}>Create new public deck</button>
<button on:click={() => newDeck("private")}>Create new private deck</button>

<style>
	div {
		display: grid;
		grid-template-columns: 1fr 1fr;
		max-height: 25em;
		overflow-y: scroll;
	}

	span.due {
		color: #007559;
	}

	blockquote {
		margin: 1em;
	}

	button {
		margin-top: 2em;
	}
</style>
