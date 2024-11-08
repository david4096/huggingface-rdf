## _!!This repository is no longer maintained.__

# __Head over to [croissant-rdf](https://github.com/david4096/croissant-rdf) for future work!!__

# huggingface_rdf

<a target="_blank" href="https://colab.research.google.com/github/david4096/huggingface-rdf/blob/main/example.ipynb">
  <img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/>
</a>

[![Open in Spaces](https://huggingface.co/datasets/huggingface/badges/resolve/main/open-in-hf-spaces-sm-dark.svg)](https://huggingface.co/spaces/david4096/huggingface-rdf)

<img width="1069" alt="image" src="https://github.com/user-attachments/assets/8d987b6b-1f55-4ed2-80cc-63f43982605f">


`huggingface_rdf` is a Python tool that generates RDF (Resource Description Framework) data from datasets available on Hugging Face. This tool enables researchers and developers to convert data into a machine-readable format for enhanced querying and data analysis.

This is made possible due to an effort to align to the [MLCommons Croissant](https://github.com/mlcommons/croissant) schema, which HF and others conform to.

## Features

- Fetch datasets from Hugging Face.
- Convert datasets to RDF format.
- Generate Turtle (.ttl) files for easy integration with SPARQL endpoints.

## Installation

To install `huggingface_rdf`, clone the repository and install the package using pip:

```bash
git clone https://github.com/david4096/huggingface-rdf.git
cd huggingface-rdf
pip install .
```

## Usage

After installing the package, you can use the command-line interface (CLI) to generate RDF data:

```
export HF_API_KEY={YOUR_KEY}
huggingface-rdf --fname huggingface.ttl --limit 10

```

Check out the `qlever_scripts` directory to get help loading the RDF into qlever for querying.

You can also easily use Jena fuseki and load the generated .ttl file from the Fuseki ui.

```

docker run -it -p 3030:3030 stain/jena-fuseki

```
### Extracting data from Kaggle
You'll need to get a Kaggle API key and it comes in a file called `kaggle.json`, you have to put the username and key into environment variables.

```
export KAGGLE_USERNAME={YOUR_USERNAME}
export KAGGLE_KEY={YOUR_KEY}
kaggle-rdf --fname kaggle.ttl --limit 10
```

### Using Docker
To launch a jupyter notebook server to run and develop on the project locally run the following:

```
docker build -t huggingface-rdf .

docker run -p 8888:8888 -v $(pwd):/app huggingface-rdf
```
The run command works for mac and linux for windows in PowerShell you need to use the following:
```
docker run -p 8888:8888 -v ${PWD}:/app huggingface-rdf
```

After that, you can access the Jupyter notebook server at http://localhost:8888.

# Useful SPARQL Queries

SPARQL (SPARQL Protocol and RDF Query Language) is a query language used to retrieve and manipulate data stored in RDF (Resource Description Framework) format, typically within a triplestore. Here are a few useful SPARQL query examples you can try to implement on https://huggingface.co/spaces/david4096/huggingface-rdf

The basic structure of a SPQRQL query is SELECT: which you have to include a keywords that you would like to return in the result.
WHERE: Defines the triple pattern we want to match in the RDF dataset.

1. This query is used to retrieve distinct predicates from an Huggingface RDF dataset

```sparql
SELECT DISTINCT ?b WHERE {?a ?b ?c}
```

2. To retrieve information about a dataset, including its name, predicates, and the count of objects associated with each predicate. Includes a filters in the results to include only resources that are of type <https://schema.org/Dataset>.

```sparql
SELECT ?name ?p (count(?o) as ?predicate_count)
WHERE {
    ?dataset <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <https://schema.org/Dataset> .
    ?dataset <https://schema.org/name> ?name .
    ?dataset ?p ?o .
}
GROUP BY ?p ?dataset
```

3. To retrieve distinct values with the keyword "bio" associated with the property <https://schema.org/keywords> regardless of the case.

```sparql
SELECT DISTINCT ?c 
WHERE {
  ?a <https://schema.org/keywords> ?c .
  FILTER(CONTAINS(LCASE(?c), "bio"))
}
```

4. To retrieve distinct values for croissant columns associated with the predicate.

```sparql
SELECT DISTINCT ?c 
WHERE {
  ?a <http://mlcommons.org/croissant/column> ?c
}
```

5. To retrieves the names of creators and the count of items they are associated with.

```sparql
SELECT ?creatorName (COUNT(?a) AS ?count)
WHERE {
  ?a <https://schema.org/creator> ?c.
  ?c <https://schema.org/name> ?creatorName.
}
GROUP BY ?creatorName
ORDER BY DESC(?count)
```

## Contributing

We welcome contributions! Please open an issue or submit a pull request!

