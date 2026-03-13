from django.core.management.base import BaseCommand
from core.models import GlossaryTerm


GLOSSARY_DATA = [
    # Computer Science
    {'term': 'algorithm', 'definition': 'A step-by-step procedure to solve a problem or perform a computation', 'subject_area': 'Computer Science'},
    {'term': 'data structure', 'definition': 'A way of organizing and storing data for efficient access and modification', 'subject_area': 'Computer Science'},
    {'term': 'recursion', 'definition': 'A technique where a function calls itself to solve smaller sub-problems', 'subject_area': 'Computer Science'},
    {'term': 'polymorphism', 'definition': 'The ability of objects to take multiple forms — a key principle in OOP', 'subject_area': 'Computer Science'},
    {'term': 'encapsulation', 'definition': 'Bundling data and methods that operate on the data within a single unit (class)', 'subject_area': 'Computer Science'},
    {'term': 'inheritance', 'definition': 'A mechanism where a new class derives properties and behaviors from an existing class', 'subject_area': 'Computer Science'},
    {'term': 'abstraction', 'definition': 'Hiding complex implementation details and showing only the necessary features', 'subject_area': 'Computer Science'},
    {'term': 'variable', 'definition': 'A named storage location in memory that holds a value', 'subject_area': 'Computer Science'},
    {'term': 'function', 'definition': 'A reusable block of code that performs a specific task and may return a value', 'subject_area': 'Computer Science'},
    {'term': 'loop', 'definition': 'A control structure that repeats a block of code until a condition is met', 'subject_area': 'Computer Science'},
    {'term': 'array', 'definition': 'An ordered collection of elements, each identified by an index', 'subject_area': 'Computer Science'},
    {'term': 'stack', 'definition': 'A last-in, first-out (LIFO) data structure', 'subject_area': 'Computer Science'},
    {'term': 'queue', 'definition': 'A first-in, first-out (FIFO) data structure', 'subject_area': 'Computer Science'},
    {'term': 'binary tree', 'definition': 'A hierarchical data structure where each node has at most two children', 'subject_area': 'Computer Science'},
    {'term': 'hash table', 'definition': 'A data structure that maps keys to values using a hash function for fast lookup', 'subject_area': 'Computer Science'},
    {'term': 'linked list', 'definition': 'A linear data structure where elements are stored in nodes connected by pointers', 'subject_area': 'Computer Science'},
    {'term': 'graph', 'definition': 'A data structure consisting of vertices (nodes) connected by edges', 'subject_area': 'Computer Science'},
    {'term': 'compiler', 'definition': 'A program that translates source code into machine code before execution', 'subject_area': 'Computer Science'},
    {'term': 'interpreter', 'definition': 'A program that executes code line by line without prior compilation', 'subject_area': 'Computer Science'},
    {'term': 'api', 'definition': 'Application Programming Interface — a set of rules for how programs communicate', 'subject_area': 'Computer Science'},
    {'term': 'debugging', 'definition': 'The process of finding and fixing errors (bugs) in code', 'subject_area': 'Computer Science'},
    {'term': 'object', 'definition': 'An instance of a class that contains data and methods', 'subject_area': 'Computer Science'},
    {'term': 'class', 'definition': 'A blueprint for creating objects that defines attributes and methods', 'subject_area': 'Computer Science'},
    {'term': 'interface', 'definition': 'A contract that defines methods a class must implement, without providing the implementation', 'subject_area': 'Computer Science'},
    {'term': 'thread', 'definition': 'The smallest unit of CPU execution within a process', 'subject_area': 'Computer Science'},
    {'term': 'concurrency', 'definition': 'Multiple tasks making progress within overlapping time periods', 'subject_area': 'Computer Science'},
    {'term': 'big o notation', 'definition': 'A mathematical notation describing the upper bound of an algorithm\'s time or space complexity', 'subject_area': 'Computer Science'},

    # Database
    {'term': 'database', 'definition': 'An organized collection of structured data stored and accessed electronically', 'subject_area': 'Database'},
    {'term': 'sql', 'definition': 'Structured Query Language — the standard language for managing relational databases', 'subject_area': 'Database'},
    {'term': 'query', 'definition': 'A request for data retrieval or manipulation from a database', 'subject_area': 'Database'},
    {'term': 'normalization', 'definition': 'The process of organizing data to reduce redundancy and improve integrity', 'subject_area': 'Database'},
    {'term': 'data redundancy', 'definition': 'Unnecessary duplication of data stored in multiple places', 'subject_area': 'Database'},
    {'term': 'primary key', 'definition': 'A unique identifier for each record in a database table', 'subject_area': 'Database'},
    {'term': 'foreign key', 'definition': 'A field in one table that references the primary key of another table', 'subject_area': 'Database'},
    {'term': 'index', 'definition': 'A database structure that speeds up data retrieval at the cost of additional storage', 'subject_area': 'Database'},
    {'term': 'join', 'definition': 'An SQL operation that combines rows from two or more tables based on a related column', 'subject_area': 'Database'},
    {'term': 'transaction', 'definition': 'A sequence of database operations treated as a single logical unit of work', 'subject_area': 'Database'},
    {'term': 'schema', 'definition': 'The structure or blueprint of a database including tables, fields, and relationships', 'subject_area': 'Database'},

    # Networking
    {'term': 'protocol', 'definition': 'A set of rules governing the format and transmission of data over a network', 'subject_area': 'Networking'},
    {'term': 'tcp', 'definition': 'Transmission Control Protocol — ensures reliable, ordered delivery of data', 'subject_area': 'Networking'},
    {'term': 'ip address', 'definition': 'A unique numerical label assigned to each device on a network', 'subject_area': 'Networking'},
    {'term': 'http', 'definition': 'HyperText Transfer Protocol — the foundation of data communication on the web', 'subject_area': 'Networking'},
    {'term': 'dns', 'definition': 'Domain Name System — translates domain names into IP addresses', 'subject_area': 'Networking'},
    {'term': 'bandwidth', 'definition': 'The maximum rate of data transfer across a network path', 'subject_area': 'Networking'},
    {'term': 'latency', 'definition': 'The delay between sending a request and receiving a response', 'subject_area': 'Networking'},
    {'term': 'firewall', 'definition': 'A security system that monitors and controls incoming and outgoing network traffic', 'subject_area': 'Networking'},
    {'term': 'encryption', 'definition': 'The process of converting data into a coded form to prevent unauthorized access', 'subject_area': 'Networking'},
    {'term': 'websocket', 'definition': 'A protocol providing full-duplex communication channels over a single TCP connection', 'subject_area': 'Networking'},

    # Mathematics
    {'term': 'derivative', 'definition': 'The rate at which a function changes with respect to a variable', 'subject_area': 'Mathematics'},
    {'term': 'integral', 'definition': 'The reverse of differentiation; computes area under a curve', 'subject_area': 'Mathematics'},
    {'term': 'matrix', 'definition': 'A rectangular array of numbers arranged in rows and columns', 'subject_area': 'Mathematics'},
    {'term': 'probability', 'definition': 'A measure of the likelihood that an event will occur, between 0 and 1', 'subject_area': 'Mathematics'},
    {'term': 'standard deviation', 'definition': 'A measure of the amount of variation in a set of values', 'subject_area': 'Mathematics'},
    {'term': 'hypothesis', 'definition': 'A proposed explanation or prediction that can be tested through experimentation', 'subject_area': 'Mathematics'},
    {'term': 'regression', 'definition': 'A statistical method for modeling the relationship between variables', 'subject_area': 'Mathematics'},
    {'term': 'correlation', 'definition': 'A statistical measure of how two variables move in relation to each other', 'subject_area': 'Mathematics'},

    # AI / Machine Learning
    {'term': 'machine learning', 'definition': 'A subset of AI where systems learn and improve from data without explicit programming', 'subject_area': 'AI'},
    {'term': 'neural network', 'definition': 'A computing system inspired by biological neurons, used for pattern recognition', 'subject_area': 'AI'},
    {'term': 'deep learning', 'definition': 'Machine learning using neural networks with many layers to model complex patterns', 'subject_area': 'AI'},
    {'term': 'training data', 'definition': 'The dataset used to teach a machine learning model to make predictions', 'subject_area': 'AI'},
    {'term': 'overfitting', 'definition': 'When a model learns noise in training data and performs poorly on new data', 'subject_area': 'AI'},
    {'term': 'classification', 'definition': 'Categorizing data into predefined groups or labels', 'subject_area': 'AI'},
    {'term': 'natural language processing', 'definition': 'AI that enables computers to understand, interpret, and generate human language', 'subject_area': 'AI'},

    # General Academic
    {'term': 'peer review', 'definition': 'Evaluation of work by experts in the same field to ensure quality and validity', 'subject_area': 'General'},
    {'term': 'citation', 'definition': 'A reference to a source used in academic writing', 'subject_area': 'General'},
    {'term': 'thesis', 'definition': 'A central argument or statement that a paper or dissertation aims to prove', 'subject_area': 'General'},
    {'term': 'methodology', 'definition': 'The systematic approach and techniques used to conduct research', 'subject_area': 'General'},
    {'term': 'paradigm', 'definition': 'A model, pattern, or framework of ideas within a discipline', 'subject_area': 'General'},
    {'term': 'empirical', 'definition': 'Based on observation or experience rather than theory alone', 'subject_area': 'General'},
    {'term': 'qualitative', 'definition': 'Research focused on understanding meanings, concepts, and descriptions', 'subject_area': 'General'},
    {'term': 'quantitative', 'definition': 'Research focused on numerical data and statistical analysis', 'subject_area': 'General'},
]


class Command(BaseCommand):
    help = 'Seed the glossary with 70+ academic terms across multiple subjects'

    def handle(self, *args, **options):
        created_count = 0
        updated_count = 0

        for entry in GLOSSARY_DATA:
            obj, created = GlossaryTerm.objects.update_or_create(
                term=entry['term'],
                defaults={
                    'definition': entry['definition'],
                    'subject_area': entry['subject_area'],
                },
            )
            if created:
                created_count += 1
            else:
                updated_count += 1

        self.stdout.write(self.style.SUCCESS(
            f'Glossary seeded: {created_count} created, {updated_count} updated ({len(GLOSSARY_DATA)} total)'
        ))
