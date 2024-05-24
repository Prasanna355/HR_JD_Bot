from crewai import Task

class Tasks():
    def draft_JD_task(self, agent, requirements, company_details):
        return Task(
            description=f"""Draft a comprehensive job description based on the gathered requirements. \
                Use the provided requirements to outline the responsibilities, qualifications, and \
                any other relevant details for the position. \

                REQUIREMENTS:\n\n {requirements} \n\n
                Company details:\n\n {company_details} \n\n
            """,
            expected_output="""A well-crafted job description that accurately represents the position \
                and its requirements""",
            context=[],
            agent=agent,
            output_file="draft_job_description.txt",
        )

    def modify_JD_task(self, agent, new_requirements, company_details):
        return Task(
            description=f"""Modify the existing job description based on the new requirements provided.\

                NEW REQUIREMENTS:\n\n {new_requirements} \n\n
                Company details:\n\n {company_details} \n\n
            """,
            expected_output="""An updated job description that incorporates the new requirements and \
                accurately represents the position.""",
            context=[],
            agent=agent,
            output_file="draft_job_description.txt",
        )
