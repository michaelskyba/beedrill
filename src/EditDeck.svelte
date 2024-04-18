<script>
	import { editingDeck } from "./store.js";

	let cards = [];

	async function getCards() {
	}
</script>

{#if cards.length == 0}
	<p>{$editingDeck.name} has no cards yet.</p>
{:else}
	<p>{$editingDeck.name} has {cards.length} cards.</p>

	{#each cards as card}
		<p>{card}</p>
	{/each}
{/if}
