from schemas.review_request import ReviewRequest
from schemas.review_response import ReviewResponse

class ReviewWorkflow:
    async def execute(self,request:ReviewRequest) -> ReviewResponse:
       ...