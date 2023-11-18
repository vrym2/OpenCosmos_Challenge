"""
Sentinel Hub Eval Scripts
"""


class sentinelhub_eval_scripts:
    """List of Sentinelhub eval scripts"""

    # True color eval script
    true_color = """
        //VERSION=3

        function setup() {
            return {
                input: [{
                    bands: ["B02", "B03", "B04"]
                }],
                output: {
                    bands: 3
                }
            };
        }

        function evaluatePixel(sample) {
            return [sample.B04, sample.B03, sample.B02];
        }
    """

    # Cloud mask data
    cloud_mask = """
        //VERSION=3

        function setup() {
        return {
            input: ["B02", "B03", "B04", "CLM"],
            output: { bands: 3 }
            }
        }

        function evaluatePixel(sample) {
        if (sample.CLM == 1) {
            return [0.75 + sample.B04, sample.B03, sample.B02]
            }
        return [3.5*sample.B04, 3.5*sample.B03, 3.5*sample.B02];
        }
    """

    # All bands
    all_bands = """
        //VERSION=3
        function setup() {
            return {
                input: [{
                    bands: ["B01","B02","B03","B04","B05","B06","B07","B08","B8A","B09","B10","B11","B12"]
                    units: "DN"
                }],
                output: {
                    bands: 13,
                    sampleType: "INT16"
                }
            };
        }

        function evaluatePixel(sample) {
            return [sample.B01,
                    sample.B02,
                    sample.B03,
                    sample.B04,
                    sample.B05,
                    sample.B06,
                    sample.B07,
                    sample.B08,
                    sample.B8A,
                    sample.B09,
                    sample.B10,
                    sample.B11,
                    sample.B12];
        }
    """  # noqa: E501

    # Digital Elevation Model
    dem = """
        //VERSION=3
        function setup() {
            return {
                input: ["DEM"],
                output:{
                id: "default",
                bands: 1,
                sampleType: SampleType.FLOAT32
                }
            }
        }

        function evaluatePixel(sample) {
            return [sample.DEM]
        }
    """
