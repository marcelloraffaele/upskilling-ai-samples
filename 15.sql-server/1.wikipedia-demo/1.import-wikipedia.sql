/*
	Create table
*/
drop table if exists [dbo].[wikipedia_articles_embeddings];
create table [dbo].[wikipedia_articles_embeddings]
(
	[id] [int] not null,
	[url] [varchar](1000) not null,
	[title] [varchar](1000) not null,
	[text] [varchar](max) not null,
	[title_vector_ada2] vector(1536),
	[content_vector_ada2] vector(1536)
)
go

/*
	Insert some data
*/
insert into [dbo].[wikipedia_articles_embeddings] ([id], [url], [title], [text], [title_vector_ada2], [content_vector_ada2]) values
(1, 'https://en.wikipedia.org/wiki/Alan_Turing', 'Alan Turing', 'Alan Turing was a pioneering computer scientist and mathematician. He is widely considered to be the father of theoretical computer science and artificial intelligence. Turing played a crucial role in breaking the Enigma code during World War II, which greatly contributed to the Allied victory.',
	null,null),
(2, 'https://en.wikipedia.org/wiki/Ada_Lovelace', 'Ada Lovelace', 'Ada Lovelace was an English mathematician and writer, chiefly known for her work on Charles Babbages proposed mechanical general-purpose computer, the Analytical Engine. She is often regarded as the first computer programmer.',
	null,null),
(3, 'https://en.wikipedia.org/wiki/Grace_Hopper', 'Grace Hopper', 'Grace Hopper was an American computer scientist and United States Navy rear admiral. She was a pioneer of computer programming who invented one of the first linkers and popularized the idea of machine-independent programming languages.',
	null,null),
(4, 'https://en.wikipedia.org/wiki/John_von_Neumann', 'John von Neumann', 'John von Neumann was a Hungarian-American mathematician, physicist, and computer scientist. He made major contributions to quantum mechanics, functional analysis, computer science, economics, and statistics.',
	null,null),
(5, 'https://en.wikipedia.org/wiki/Donald_Knuth', 'Donald Knuth', 'Donald Knuth is an American computer scientist, mathematician, and professor emeritus at Stanford University. He is best known for his work on algorithms and for writing The Art of Computer Programming.',
	null,null),
(6, 'https://en.wikipedia.org/wiki/Tim_Berners-Lee', 'Tim Berners-Lee', 'Tim Berners-Lee is an English computer scientist best known as the inventor of the World Wide Web. He implemented the first successful communication between a Hypertext Transfer Protocol (HTTP) client and server.',
	null,null),
(7, 'https://en.wikipedia.org/wiki/Katherine_Johnson', 'Katherine Johnson', 'Katherine Johnson was an American mathematician whose calculations of orbital mechanics were critical to the success of the first and subsequent U.S. manned spaceflights.',
	null,null),
(8, 'https://en.wikipedia.org/wiki/Claude_Shannon', 'Claude Shannon', 'Claude Shannon was an American mathematician, electrical engineer, and cryptographer known as the father of information theory.',
	null,null),
(9, 'https://en.wikipedia.org/wiki/Barbara_Liskov', 'Barbara Liskov', 'Barbara Liskov is an American computer scientist who developed the Liskov substitution principle and made significant contributions to programming languages and distributed computing.',
	null,null),
(10, 'https://en.wikipedia.org/wiki/Edgar_F._Codd', 'Edgar F. Codd', 'Edgar F. Codd was an English computer scientist who invented the relational model for database management, the foundation for relational databases.',
	null,null),
(11, 'https://en.wikipedia.org/wiki/Marvin_Minsky', 'Marvin Minsky', 'Marvin Minsky was an American cognitive scientist in the field of artificial intelligence, co-founder of MITs AI laboratory.',
	null,null),
(12, 'https://en.wikipedia.org/wiki/John_McCarthy_(computer_scientist)', 'John McCarthy', 'John McCarthy was an American computer scientist and cognitive scientist. He coined the term "artificial intelligence" and developed the Lisp programming language.',
	null,null),
(13, 'https://en.wikipedia.org/wiki/Frances_E._Allen', 'Frances E. Allen', 'Frances E. Allen was an American computer scientist and pioneer in the field of optimizing compilers. She was the first female IBM Fellow.',
	null,null),
(14, 'https://en.wikipedia.org/wiki/Steve_Wozniak', 'Steve Wozniak', 'Steve Wozniak is an American electronics engineer, programmer, and co-founder of Apple Inc. He developed the Apple I and Apple II computers.',
	null,null),
(15, 'https://en.wikipedia.org/wiki/Guido_van_Rossum', 'Guido van Rossum', 'Guido van Rossum is a Dutch programmer best known as the creator of the Python programming language.',
	null,null),
(16, 'https://en.wikipedia.org/wiki/Linus_Torvalds', 'Linus Torvalds', 'Linus Torvalds is a Finnish-American software engineer who is the creator and principal developer of the Linux kernel.',
	null,null),
(17, 'https://en.wikipedia.org/wiki/Margaret_Hamilton_(software_engineer)', 'Margaret Hamilton', 'Margaret Hamilton is an American computer scientist, systems engineer, and business owner. She led the software engineering division for the Apollo program.',
	null,null),
(18, 'https://en.wikipedia.org/wiki/Dennis_Ritchie', 'Dennis Ritchie', 'Dennis Ritchie was an American computer scientist who created the C programming language and co-developed the Unix operating system.',
	null,null),
(19, 'https://en.wikipedia.org/wiki/Bjarne_Stroustrup', 'Bjarne Stroustrup', 'Bjarne Stroustrup is a Danish computer scientist most notable for the creation and development of the C++ programming language.',
	null,null),
(20, 'https://en.wikipedia.org/wiki/James_Gosling', 'James Gosling', 'James Gosling is a Canadian computer scientist, best known as the founder and lead designer behind the Java programming language.',
	null,null);
go


alter table [dbo].[wikipedia_articles_embeddings]
add constraint pk__wikipedia_articles_embeddings primary key clustered (id)
go

/*
	Add index on title
*/
create index [ix_title] on [dbo].[wikipedia_articles_embeddings](title)
go

/*
	Verify data
*/
select top (10) * from [dbo].[wikipedia_articles_embeddings]
go

select * from [dbo].[wikipedia_articles_embeddings] where title = 'Alan Turing'
go



select * from [dbo].[wikipedia_articles_embeddings]