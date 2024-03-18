import timeTests.layers.Interrogator
import timeTests.layers.llama2
import timeTests.layers.mistral
import timeTests.layers.stable

if __name__ == "__main__":
    timeTests.layers.Interrogator.timeInterrogator()
    timeTests.layers.llama2.timeLLama2()
    timeTests.layers.mistral.getMistralTime()
    timeTests.layers.stable.getStableTime()