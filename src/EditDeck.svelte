<script>
	import { page, editingDeck } from "./store.js";

	let cards = [];

	async function getCards() {
		cards = [
			{
				id: 1,
				front: "front1",
				back: "back1",
			},
			{
				id: 2,
				front: "front2",
				back: "back2",
			},
		]
	}

	page.subscribe(v => {
		if (v == "edit_deck")
			getCards();
	});
</script>

{#if cards.length == 0}
	<p>{$editingDeck.name} has no cards yet.</p>
{:else}
	<p>{$editingDeck.name} has {cards.length} cards.</p>
{/if}

{#if cards.length > 0}
	{#each cards as card}
		<blockquote>
			<p>{card.front}</p>
			<hr>
			<p>{card.back}</p>
			<hr class="half">

			<button>Delete</button>
		</blockquote>
	{/each}
{/if}

<style>
	hr.half {
		width: 25%;
		margin-left: 0;
	}
</style>
