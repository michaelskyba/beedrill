<script>
	import { page, myDecks } from "./store.js";

	let deckName;

	async function getDecks() {
		const response = await fetch("http://127.0.0.1:8000/decks/get/mine");
		const data = await response.json();
		myDecks.set(data);
	}

	page.subscribe(v => {
		if (v == "my_decks")
			getDecks();
	})

	async function newDeck(type) {
		if (!deckName)
			return;

		const isPublic = type == "public" ? 1 : 0;
		alert(deckName + isPublic)
	}

	async function createPublic() {
		newDeck("public");
	}

	async function createPrivate() {
		newDeck("private");
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
		</blockquote>
	{/each}
</div>

<hr>

<input placeholder="Deck name" bind:value={deckName}>
<button on:click={createPublic}>Create new public deck</button>
<button on:click={createPrivate}>Create new private deck</button>

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
