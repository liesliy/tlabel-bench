# Contributing to TLabel-Bench

Thank you for your interest in contributing! This guide covers how to add new sensor annotations, objects, and evaluation scripts.

---

## Ways to Contribute

### 1. New Sensor Annotations

If you have access to a tactile sensor not yet covered (SynTouch, XELA, BioTac, etc.):

1. Select objects from our standard object list (see `annotations/` for existing IDs)
2. Annotate using TLabel ≥ 0.4.2
3. Export in JSON format following our [annotation schema](annotation_schema.md)
4. Submit a PR with annotations in `annotations/<sensor_name>/`

**Requirements:**
- At least 5 objects from our standard set must be included
- Minimum 3 interactions per object
- Quality scores must be computed
- Episode segmentation must be provided

### 2. New Objects

To add new objects:

1. Annotate the same objects with ALL available sensors
2. Use consistent `object_id` naming: `obj_XXX` where XXX is a 3-digit number starting from the next available ID
3. Include a `material_detail` field describing the specific material
4. Submit a PR updating all relevant sensor directories

### 3. Evaluation Scripts

New evaluation tasks are welcome:

1. Follow the existing script structure in `evaluation/`
2. Include a README within the script explaining the task and metrics
3. Provide baseline results
4. Ensure the script works with the standard annotation format

---

## Data License Requirements

When contributing annotations based on existing datasets:

- **You must verify the original dataset's license** before submitting
- If the original data is under a restrictive license (NC, ARR), only annotation files can be accepted
- Clearly state the data source and license in your PR description
- Self-collected data is always welcome (we'll mark it as such)

---

## PR Checklist

- [ ] Annotations follow the [schema](annotation_schema.md)
- [ ] Quality scores are computed (not manually assigned)
- [ ] Episode segmentation is provided
- [ ] Data source and license are documented
- [ ] `merge_annotations.py` still works with the new data
- [ ] Evaluation scripts produce valid results with the new data

---

## Code of Conduct

Be respectful. We're all here to advance tactile sensing research. Constructive feedback welcome; personal attacks are not.

---

## Questions?

Open an issue on GitHub or reach out to the TLabel team.
