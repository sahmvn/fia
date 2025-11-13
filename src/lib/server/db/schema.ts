import { sql } from 'drizzle-orm';
import { integer, sqliteTable, text, unique } from 'drizzle-orm/sqlite-core';

export const postsTable = sqliteTable('posts', {
	id: integer({ mode: 'number' }).primaryKey({ autoIncrement: true }),
	title: text().notNull(),
	body: text().notNull(),
	when_created: integer({ mode: 'timestamp' })
		.notNull()
		.default(sql`(strftime('%s', 'now'))`)
});

export const flavorsOfAbuseTable = sqliteTable('flavors_of_abuse', {
	id: integer({ mode: 'number' }).primaryKey({ autoIncrement: true }),
	name: text().notNull().unique()
});

export const traumasTable = sqliteTable('traumas', {
	id: integer({ mode: 'number' }).primaryKey({ autoIncrement: true }),
	name: text().notNull().unique(),
	abuse_techniques: text().notNull(),
	research_summary: text().notNull()
});

export const vulnerabilityTypesTable = sqliteTable('vulnerability_types', {
	id: integer({ mode: 'number' }).primaryKey({ autoIncrement: true }),
	name: text().notNull().unique(),
	vulnerability_traits: text().notNull(),
	abuse_techniques: text().notNull(),
	brain_biases: text().notNull()
});

export const playerTypologiesTable = sqliteTable('player_typologies', {
	id: integer({ mode: 'number' }).primaryKey({ autoIncrement: true }),
	name: text().notNull().unique(),
	alias: text().notNull(),
	summary: text().notNull(),
	main_motivation: text().notNull(),
	always_does_this: text().notNull(),
	he_never_does_this: text().notNull(),
	red_flags: text().notNull(),
	techniques_he_might_use: text().notNull(),
	vulnerability_traits: text().notNull()
});

export const playerToVulnerabilityTypesTable = sqliteTable(
	'player_to_vulnerability_types',
	{
		player_id: integer({ mode: 'number' }).references(() => playerTypologiesTable.id),
		vulnerability_type_id: integer({ mode: 'number' }).references(() => vulnerabilityTypesTable.id)
	},
	(t) => [unique().on(t.player_id, t.vulnerability_type_id)]
);

export const playerToTraumasTable = sqliteTable(
	'player_to_traumas',
	{
		player_id: integer({ mode: 'number' }).references(() => playerTypologiesTable.id),
		trauma_id: integer({ mode: 'number' }).references(() => traumasTable.id)
	},
	(t) => [unique().on(t.player_id, t.trauma_id)]
);

export const playerToFlavorsTable = sqliteTable(
	'player_to_flavors',
	{
		player_id: integer({ mode: 'number' }).references(() => playerTypologiesTable.id),
		flavor_id: integer({ mode: 'number' }).references(() => flavorsOfAbuseTable.id)
	},
	(t) => [unique().on(t.player_id, t.flavor_id)]
);
