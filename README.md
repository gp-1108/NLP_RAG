<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a name="readme-top"></a>
<!-- PROJECT SHIELDS -->


<!-- PROJECT LOGO -->
<br />
<div align="center">
    <a href="https://github.com/gp-1108/NLP_RAG">
        <img src="images/lamar_ai.jpg" alt="Logo" width="80" height="80">
    </a>

<h3 align="center">Llama3 NLP Rag</h3>

<p align="center" width="300px">
    A RAG system based on Langchain and Llama3 created for answering general question about Kendrick Lamar's career and life.
    It proved a simple yet effective point on how to setup, compile and use NLP tools for interesting and fast results.
</p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#dataset">Building the dataset</a></li>
        <li><a href="#faiss">Creating the index</a></li>
        <li><a href="#rag">Creating the RAG model</a></li>
      </ul>
    </li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

This project serves the purpose of showing how to correctly build from start to finish a RAG system using Langchain and Llama3.
Not only that, it is also shown how to recreate the dataset used (as well as a copy ready for use).
From dataset creation to prompt answering, it can be useful to guide new comers.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

The project is divided into the following steps:
1. Create the dataset -> This was done using the [wikiextractor library](https://github.com/attardi/wikiextractor) and the source code can be found in the `building_dataset` folder.
2. Creating the FAISS index -> Especially for larger datasets, it can be quite computationally expensive to build one each and every time. As such I used a cluster made available my university based on [SLURM](https://slurm.schedmd.com/overview.html) and [Singularity](https://docs.sylabs.io/guides/latest/user-guide/). In the `faiss_env` folder you can find the source code on how it was done.
3. Creating the RAG model -> This was done creating a Jupiter notebook on Google Colab. The source code can be found in the main folder of the project.

Skip to the appropriate section for more information.

### Built With

* [LangChain](https://www.langchain.com/)
* [Google Colab](https://colab.research.google.com/)
* [Llama3](https://llama.meta.com/llama3/)
* [Hugging Face](https://huggingface.co/)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started
Feel free to skip to whatever section you are interested in.
As the project is divided into three main parts, you might have different requirements for each one.

### Dataset
The dataset was extract from the [Wikipedia dumps](https://dumps.wikimedia.org/). The main idea is to parse the dump, extract only the relevant articles and then saving them in a format suitable for the Langchain API. All of the code mentioned can be found in the `building_dataset` folder.

An already made extraction for the Kendrick Lamar related articles can be found in the folder under the name `extract_kendrick.tar.gz`.

To extract and parse all of the articles I used the [wikiextractor library](https://github.com/attardi/wikiextractor). Simply check the documentation and extract them wherever you want. Given this was a dummy project, I extracted the data without parsing the `templates` as well, make sure to change that if you want to have a more complete dataset. The rest of the procedure remains unchanged.

Once extracted the data, use the `kendrick_polisher.py` script to parse the data and save it in a format suitable for the Langchain API. The script will create a folder with the extracted .txt files. The script uses concurrent processing to speed up the process in batches, change the `batch_size` variable to your liking.
```sh
python3 kendrick_polisher.py <path_to_extracted_data> <path_to_save_data> <batch_size>
```

Now the data is ready to be used for the next steps, I zipped it and uploaded it to Google Drive for easy access and retrieved it easily with the use of the [gdown library](https://github.com/wkentaro/gdown).

### FAISS
Creating the FAISS index can be quite long, in my case it wasn't suitable on my laptop and I used a cluster for more computing power. Given that each and every setup is quite different, you might skip this part unless you have a very similar setup to mine.
All referenced files can be found in the `faiss_env` folder.

Still, the process was the following:
1. Create a Singularity image with the necessary dependencies. `sudo singularity build faiss.sif faiss.def`
2. Copy the slurm script and the python script to the cluster and run it. `sbatch faiss.slurm`

You can also use the `build_faiss_index.py` file on your own local machine, to do so run it like this:
```sh
python3 build_faiss_index.py <path_to_dataset> <path_to_save_index>
```

This will create the index and save it to the specified path. Later on I uploaded it to Google Drive as well and used the [gdown library](https://github.com/wkentaro/gdown) to download it in Google Colab.


### RAG
The heart of the project: the RAG model. The development was done on Google Colab but the code can be run on any machine with the necessary dependencies. The code can be found in the main folder as `NLP_Rag_project.ipynb`.
The code is quite well documented and should be easy to follow.

Please be aware that you need a GPU to load the model and also an account on the Hugging Face website to access the model. Make sure to request permissions at the [Llama 3 model card](https://huggingface.co/meta-llama/Meta-Llama-3-8B-Instruct).

The main steps are:
1. Load the dataset
2. Load the FAISS index
3. Do some analysis on the dataset
4. Setup Llama3
5. Create the RAG model

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage Examples
Here you can find some examples prompt-answer using the RAG model created:

```text
Question: Tell me an interesting fact about Kendrick.
Answer: 
         According to the provided context, an interesting fact about Kendrick Lamar is that his song "Alright" became a rallying cry for the Black Lives Matter movement in 2015, symbolizing hope and optimism in the face of discrimination and persecution.
```

```text
Question: Did Lamar set any record or achieved widely known prizes?
Answer: 
         Yes, Kendrick Lamar has achieved several records and widely recognized prizes throughout his career. Some of his notable achievements include:

* Most awarded artist in BET Hip Hop Awards history with 29 wins
* First artist to win Video of the Year for a music video he co-directed with "Humble"
* First artist from any genre to be nominated for Album of the Year with four consecutive lead studio albums since Billy Joel (1979–1983)
* Third-most won by a rapper in Grammy Awards history with 17 wins
* Most wins by any artist in BET Hip Hop Awards history with 29 wins
* Won the Pulitzer Prize for Music for his album "Damn"
* Won the Primetime Emmy Award for Outstanding Variety Special (Live) as a headliner of the Pepsi Super Bowl LVI Halftime Show
* Won the Brit Award, four American Music Awards, six "Billboard" Music Awards, and 11 MTV Video Music Awards (including two Video of the Year wins)

These are just a few examples of his many achievements.
```

```text
Question: What are some of the best Lamar's songs?

Answer: It's difficult to pinpoint the best of Kendrick Lamar's songs, as opinions on his music are subjective and varied. However, some of his most critically acclaimed and popular tracks include:

* "Alright"
* "Humble"
* "The Blacker the Berry"
* "Like That"
* "Freedom"
* "Sidewalks"
* "Goosebumps"
* "Bad Blood" (remix)
* "America Has a Problem"
* "The Hillbillies"

These songs showcase his unique blend of jazz, funk, soul, and hip-hop styles, as well as his thought-provoking lyrics that often address social and political issues.
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- LICENSE -->
## License

Distributed under the MIT License.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Project Link: [https://github.com/gp-1108/NLP_RAG](https://github.com/gp-1108/NLP_RAG)

<p align="right">(<a href="#readme-top">back to top</a>)</p>
