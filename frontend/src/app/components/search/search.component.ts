import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { ApiService, SearchRequest } from '../../services/api.service';
import { StateService } from '../../services/state.service';

@Component({
  selector: 'app-search',
  templateUrl: './search.component.html',
  styleUrls: ['./search.component.scss']
})
export class SearchComponent {
  topic: string = '';
  limit: number = 5;
  provider: string = 'gemini';
  loading: boolean = false;
  result: any = null;
  error: string = '';

  constructor(
    private apiService: ApiService,
    private stateService: StateService,
    private router: Router
  ) {}

  onSearch() {
    if (!this.topic.trim()) {
      this.error = 'Please enter a research topic';
      return;
    }

    this.loading = true;
    this.error = '';
    this.result = null;

    const request: SearchRequest = {
      topic: this.topic,
      limit: this.limit,
      provider: this.provider
    };

    this.apiService.searchPapers(request).subscribe({
      next: (response) => {
        this.loading = false;
        if (response.success) {
          this.result = response;
          this.stateService.setCurrentCollection(response.collection_name);
          this.stateService.setCurrentTopic(this.topic);
        } else {
          this.error = response.error || 'Failed to search papers';
        }
      },
      error: (err) => {
        this.loading = false;
        this.error = 'An error occurred while searching papers. Please try again.';
        console.error('Search error:', err);
      }
    });
  }

  navigateToChat() {
    this.router.navigate(['/chat']);
  }

  resetSearch() {
    this.topic = '';
    this.result = null;
    this.error = '';
  }
}
