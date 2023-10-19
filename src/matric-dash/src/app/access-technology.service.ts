// access-technology.service.ts
import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root',
})
export class AccessTechService {  // Rename this class to avoid conflict
  private API_URL = 'http://localhost:5000';

  constructor(private http: HttpClient) {}

  getAccessTechnologies() {
    return this.http.get<any[]>(`${this.API_URL}/access_technologies`);
  }
}
