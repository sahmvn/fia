import { and, eq } from 'drizzle-orm';
import { tool } from 'langchain';
import * as z from 'zod';
import { postAnalystSubagent } from './agents';
import { db } from './db';
import { playerTypologiesTable, postsTable } from './db/schema';

export const savePostToDB = tool(
	async ({ title, body }) => {
		await db.insert(postsTable).values({
			title,
			body
		});
	},
	{
		name: 'savePostToDB',
		description: 'Saves the analyzed scene’s title and body to the posts database.',
		schema: z.object({
			title: z
				.string()
				.describe('A short, descriptive title summarizing the abusive or manipulative scene.'),
			body: z
				.string()
				.describe(
					'A detailed explanation or analysis of the scene, including context and interpretation.'
				)
		})
	}
);

export const callPostAnalystSubagent = tool(
	async ({ query }) => {
		await postAnalystSubagent.invoke({
			messages: [{ role: 'user', content: query }]
		});

		return '';
	},
	{
		name: 'callPostAnalystSubagent',
		description:
			'Sends the detected abusive or manipulative scene text to the PostAnalystSubagent for deeper analysis.',
		schema: z.object({
			query: z
				.string()
				.describe(
					'The text or excerpt of the movie script containing the potential abuse or manipulation.'
				)
		})
	}
);

export const getAllPlayerTypologies = tool(
	async () => {
		const players = await db
			.select({
				name: playerTypologiesTable.name
			})
			.from(playerTypologiesTable)
			.orderBy(playerTypologiesTable.id);

		return players.map((_) => _.name).join('\n');
	},
	{
		name: 'getAllPlayerTypologies',
		description:
			'Fetches a list of all available player typologies or character archetypes used for behavioral analysis.'
	}
);

export const getPlayerTypologyInformationByName = tool(
	async ({ player_name }) => {
		const [player_typology] = await db
			.select()
			.from(playerTypologiesTable)
			.where(and(eq(playerTypologiesTable.name, player_name)));

		if (!player_typology) {
			return `ERROR: no player typology with name ${player_name}`;
		}

		return player_typology.summary;
	},
	{
		name: 'getPlayerTypologyInformationByName',
		description:
			'Retrieves a detailed summary of a specific player typology, explaining its traits and behavioral patterns.',
		schema: z.object({
			player_name: z
				.string()
				.describe(
					'The name of the player typology (character archetype) to retrieve information for.'
				)
		})
	}
);
