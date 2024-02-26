from ctransformers import AutoModelForCausalLM
from diffusers import StableDiffusionImg2ImgPipeline


STABLE_MODEL = StableDiffusionImg2ImgPipeline.from_pretrained( "runwayml/stable-diffusion-v1-5" )

LLM_MODEL = AutoModelForCausalLM.from_pretrained(
                model_path_or_repo_id="TheBloke/Mistral-7B-Instruct-v0.1-GGUF", 
                model_file="mistral-7b-instruct-v0.1.Q5_K_S.gguf", 
                model_type="mistral",
                temperature=0.7,
                top_p=1,
                top_k=50,
                repetition_penalty=1.2,
                context_length=8096,
                max_new_tokens=2048,
            )

modelPrompt = LLM_MODEL( "hello", max_new_tokens = 77 )
print( modelPrompt )