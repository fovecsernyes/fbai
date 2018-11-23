DROP TABLE IF EXISTS public.test_extract;

WITH F AS (
  SELECT cycle_id, SUM(fitness_score) AS max_fitness
  FROM public.fitness
  GROUP BY cycle_id
)
SELECT  cycle_id, max_fitness, c.game_id, 
(SELECT COUNT(*) FROM public.cycle ci WHERE ci.game_id = c.game_id),
c.parameters
INTO public.test_extract
FROM F f
INNER JOIN public.cycle c
ON c.id = f.cycle_id
WHERE f.max_fitness > 5000
--ORDER BY f.max_fitness DESC
ORDER BY c.game_id DESC;

UPDATE public.test_extract SET parameters = REPLACE(REPLACE(parameters, '{', ''), '}', '');
UPDATE public.test_extract SET parameters = REPLACE(parameters, '''', '');

SELECT * FROM public.test_extract;


ALTER TABLE public.test_extract ADD COLUMN textgeneration text;
UPDATE public.test_extract SET textgeneration = x.textgeneration
FROM (
  SELECT cycle_id, (SELECT regexp_matches(parameters, 'generation: [0-9]*')::text[])[1] AS textgeneration FROM public.test_extract
) AS x
WHERE x.cycle_id = public.test_extract.cycle_id;

ALTER TABLE public.test_extract ADD COLUMN generation integer;
UPDATE public.test_extract SET generation = REPLACE(textgeneration, 'generation: ', '')::integer;


ALTER TABLE public.test_extract ADD COLUMN textgravity text;
UPDATE public.test_extract SET textgravity = x.textgravity
FROM (
  SELECT cycle_id, (SELECT regexp_matches(parameters, 'gravity: [0-9]*')::text[])[1] AS textgravity FROM public.test_extract
) AS x
WHERE x.cycle_id = public.test_extract.cycle_id;

ALTER TABLE public.test_extract ADD COLUMN gravity integer;
UPDATE public.test_extract SET gravity = REPLACE(textgravity, 'gravity: ', '')::integer;


ALTER TABLE public.test_extract ADD COLUMN textjump text;
UPDATE public.test_extract SET textjump = x.textjump
FROM (
  SELECT cycle_id, (SELECT regexp_matches(parameters, 'jump: [0-9]*')::text[])[1] AS textjump FROM public.test_extract
) AS x
WHERE x.cycle_id = public.test_extract.cycle_id;

ALTER TABLE public.test_extract ADD COLUMN jump integer;
UPDATE public.test_extract SET jump = REPLACE(textjump, 'jump: ', '')::integer;


ALTER TABLE public.test_extract ADD COLUMN textpopulation text;
UPDATE public.test_extract SET textpopulation = x.textpopulation
FROM (
  SELECT cycle_id, (SELECT regexp_matches(parameters, 'population: [0-9]*')::text[])[1] AS textpopulation FROM public.test_extract
) AS x
WHERE x.cycle_id = public.test_extract.cycle_id;

ALTER TABLE public.test_extract ADD COLUMN population integer;
UPDATE public.test_extract SET population = REPLACE(textpopulation, 'population: ', '')::integer;


ALTER TABLE public.test_extract ADD COLUMN textgap text;
UPDATE public.test_extract SET textgap = x.textgap
FROM (
  SELECT cycle_id, (SELECT regexp_matches(parameters, 'gap: [0-9]*')::text[])[1] AS textgap FROM public.test_extract
) AS x
WHERE x.cycle_id = public.test_extract.cycle_id;

ALTER TABLE public.test_extract ADD COLUMN gap integer;
UPDATE public.test_extract SET gap = REPLACE(textgap, 'gap: ', '')::integer;


ALTER TABLE public.test_extract ADD COLUMN textdistance text;
UPDATE public.test_extract SET textdistance = x.textdistance
FROM (
  SELECT cycle_id, (SELECT regexp_matches(parameters, 'distance: [0-9]*')::text[])[1] AS textdistance FROM public.test_extract
) AS x
WHERE x.cycle_id = public.test_extract.cycle_id;

ALTER TABLE public.test_extract ADD COLUMN distance integer;
UPDATE public.test_extract SET distance = REPLACE(textdistance, 'distance: ', '')::integer;


ALTER TABLE public.test_extract ADD COLUMN texthidden text;
UPDATE public.test_extract SET texthidden = x.texthidden
FROM (
  SELECT cycle_id, (SELECT regexp_matches(parameters, 'hidden: [0-9]*')::text[])[1] AS texthidden FROM public.test_extract
) AS x
WHERE x.cycle_id = public.test_extract.cycle_id;

ALTER TABLE public.test_extract ADD COLUMN hidden integer;
UPDATE public.test_extract SET hidden = REPLACE(texthidden, 'hidden: ', '')::integer;


ALTER TABLE public.test_extract ADD COLUMN textselection text;
UPDATE public.test_extract SET textselection = x.textselection
FROM (
  SELECT cycle_id, (SELECT regexp_matches(parameters, 'selection: [0-9]*')::text[])[1] AS textselection FROM public.test_extract
) AS x
WHERE x.cycle_id = public.test_extract.cycle_id;

ALTER TABLE public.test_extract ADD COLUMN selection integer;
UPDATE public.test_extract SET selection = REPLACE(textselection, 'selection: ', '')::integer;


ALTER TABLE public.test_extract ADD COLUMN textdeletion text;
UPDATE public.test_extract SET textdeletion = x.textdeletion
FROM (
  SELECT cycle_id, (SELECT regexp_matches(parameters, 'deletion: [0-9]*')::text[])[1] AS textdeletion FROM public.test_extract
) AS x
WHERE x.cycle_id = public.test_extract.cycle_id;

ALTER TABLE public.test_extract ADD COLUMN deletion integer;
UPDATE public.test_extract SET deletion = REPLACE(textdeletion, 'deletion: ', '')::integer;


ALTER TABLE public.test_extract ADD COLUMN textcrossover text;
UPDATE public.test_extract SET textcrossover = x.textcrossover
FROM (
  SELECT cycle_id, (SELECT regexp_matches(parameters, 'crossover: [0-9]*')::text[])[1] AS textcrossover FROM public.test_extract
) AS x
WHERE x.cycle_id = public.test_extract.cycle_id;

ALTER TABLE public.test_extract ADD COLUMN crossover integer;
UPDATE public.test_extract SET crossover = REPLACE(textcrossover, 'crossover: ', '')::integer;


ALTER TABLE public.test_extract ADD COLUMN textmutation1 text;
UPDATE public.test_extract SET textmutation1 = x.textmutation1
FROM (
  SELECT cycle_id, (SELECT regexp_matches(parameters, 'mutation1: [0-9]*')::text[])[1] AS textmutation1 FROM public.test_extract
) AS x
WHERE x.cycle_id = public.test_extract.cycle_id;

ALTER TABLE public.test_extract ADD COLUMN mutation1 integer;
UPDATE public.test_extract SET mutation1 = REPLACE(textmutation1, 'mutation1: ', '')::integer;


ALTER TABLE public.test_extract ADD COLUMN textmutation2 text;
UPDATE public.test_extract SET textmutation2 = x.textmutation2
FROM (
  SELECT cycle_id, (SELECT regexp_matches(parameters, 'mutation2: [0-9]*')::text[])[1] AS textmutation2 FROM public.test_extract
) AS x
WHERE x.cycle_id = public.test_extract.cycle_id;

ALTER TABLE public.test_extract ADD COLUMN mutation2 integer;
UPDATE public.test_extract SET mutation2 = REPLACE(textmutation2, 'mutation2: ', '')::integer;


ALTER TABLE public.test_extract ADD COLUMN textthreshold text;
UPDATE public.test_extract SET textthreshold = x.textthreshold
FROM (
  SELECT cycle_id, (SELECT regexp_matches(parameters, 'threshold: [0-9]*')::text[])[1] AS textthreshold FROM public.test_extract
) AS x
WHERE x.cycle_id = public.test_extract.cycle_id;

ALTER TABLE public.test_extract ADD COLUMN threshold integer;
UPDATE public.test_extract SET threshold = REPLACE(textthreshold, 'threshold: ', '')::integer;


ALTER TABLE public.test_extract ADD COLUMN textgame_id2 text;
UPDATE public.test_extract SET textgame_id2 = x.textgame_id2
FROM (
  SELECT cycle_id, (SELECT regexp_matches(parameters, 'game_id: [0-9]*')::text[])[1] AS textgame_id2 FROM public.test_extract
) AS x
WHERE x.cycle_id = public.test_extract.cycle_id;

ALTER TABLE public.test_extract ADD COLUMN game_id2 integer;
UPDATE public.test_extract SET game_id2 = REPLACE(textgame_id2, 'game_id: ', '')::integer;


ALTER TABLE public.test_extract ADD COLUMN textbird_ids text;
UPDATE public.test_extract SET textbird_ids = x.textbird_ids
FROM (
  SELECT cycle_id, (SELECT regexp_matches(parameters, 'bird_ids:.*')::text[])[1] AS textbird_ids FROM public.test_extract
) AS x
WHERE x.cycle_id = public.test_extract.cycle_id;

UPDATE public.test_extract SET textbird_ids = REPLACE(textbird_ids, 'bird_ids: [', '');
UPDATE public.test_extract SET textbird_ids = REPLACE(textbird_ids, ']', '');

ALTER TABLE public.test_extract ADD COLUMN bird_ids integer[];
UPDATE public.test_extract SET bird_ids = string_to_array(textbird_ids, ', ')::integer[];

ALTER TABLE public.test_extract ADD COLUMN bird_count integer;
UPDATE public.test_extract SET bird_count = array_length(bird_ids, 1);

